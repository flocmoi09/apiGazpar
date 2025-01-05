from typing import Any, List, Dict, cast, Optional
import logging
import glob
import os
import json
import time
from datetime import date, timedelta
from abc import ABC, abstractmethod
import aiohttp
from pygazpar.enum import Frequency, PropertyName,ConsommationRole
from pygazpar.excelparser import ExcelParser
from pygazpar.jsonparser import JsonParser
from pygazpar.auth import GazparAuth
from pygazpar.consommation import GazparConsommation
from pygazpar.pce import GazparPCE
from pygazpar.frequency import FrequencyConverter

Logger = logging.getLogger(__name__)

MeterReading = Dict[str, Any]

MeterReadings = List[MeterReading]

MeterReadingsByFrequency = Dict[str, MeterReadings]


# ------------------------------------------------------------------------------------------------------------
class IDataSource(ABC):

    @abstractmethod
    def load(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        pass


# ------------------------------------------------------------------------------------------------------------
class WebDataSource(IDataSource):

    # ------------------------------------------------------
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):

        self.__username = username
        self.__password = password
        self.__session = session
        self._pce= GazparPCE(session)
        self._conso=GazparConsommation(session)
        self._auth=GazparAuth(username, password,session)
        self._auth_token=None

    # ------------------------------------------------------
    async def load(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        if(self._auth_token is None):
            self._auth_token=await self._auth.request_token()
        
        res = await self._loadFromSession(pceIdentifier, startDate, endDate, frequencies)

        Logger.debug("The data update terminates normally")

        return res


    @abstractmethod
    async def _loadFromSession(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        pass


# ------------------------------------------------------------------------------------------------------------
class ExcelWebDataSource(WebDataSource):


    DATE_FORMAT = "%Y-%m-%d"

    FREQUENCY_VALUES = {
        Frequency.HOURLY: "Horaire",
        Frequency.DAILY: "Journalier",
        Frequency.WEEKLY: "Hebdomadaire",
        Frequency.MONTHLY: "Mensuel",
        Frequency.YEARLY: "Journalier"
    }

    DATA_FILENAME = 'Donnees_informatives_*.xlsx'

    # ------------------------------------------------------
    def __init__(self, username: str, password: str,tmpDirectory: str, session: aiohttp.ClientSession|None=None):

        if(session is None):
            session = aiohttp.ClientSession(cookie_jar= aiohttp.CookieJar())
      
        super().__init__(username, password,session)
        
        self.__tmpDirectory = tmpDirectory

    # ------------------------------------------------------
    async def _loadFromSession(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        # XLSX is in the TMP directory
        data_file_path_pattern = self.__tmpDirectory + '/' + ExcelWebDataSource.DATA_FILENAME

        # We remove an eventual existing data file (from a previous run that has not deleted it).
        file_list = glob.glob(data_file_path_pattern)
        for filename in file_list:
            if os.path.isfile(filename):
                try:
                    os.remove(filename)
                except PermissionError:
                    pass

        if frequencies is None:
            # Transform Enum in List.
            frequencyList = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequencyList = set(frequencies)

        for frequency in frequencyList:
            # Inject parameters.

            Logger.debug(f"Loading data of frequency {ExcelWebDataSource.FREQUENCY_VALUES[frequency]} from {startDate.strftime(ExcelWebDataSource.DATE_FORMAT)} to {endDate.strftime(ExcelWebDataSource.DATE_FORMAT)}")

            # Retry mechanism.
            retry = 10
            while retry > 0:


                try:
                    response = await self._conso.get_consommation_file(pceIdentifier,startDate.strftime(ExcelWebDataSource.DATE_FORMAT),endDate.strftime(ExcelWebDataSource.DATE_FORMAT),ConsommationRole.INFORMATIVES,frequency)
                    open(f"{self.__tmpDirectory}/{response.filename}", "wb").write(response.content)

                    break
                except Exception as e:

                    if retry == 1:
                        raise e

                    Logger.error("An error occurred while loading data. Retry in 3 seconds.")
                    time.sleep(3)
                    retry -= 1

            # Load the XLSX file into the data structure
            file_list = glob.glob(data_file_path_pattern)

            if len(file_list) == 0:
                Logger.warning(f"Not any data file has been found in '{self.__tmpDirectory}' directory")

            for filename in file_list:
                res[frequency.value] = ExcelParser.parse(filename, frequency if frequency != Frequency.YEARLY else Frequency.DAILY)
                try:
                    # openpyxl does not close the file properly.
                    os.remove(filename)
                except PermissionError:
                    pass

            # We compute yearly from daily data.
            if frequency == Frequency.YEARLY:
                res[frequency.value] = FrequencyConverter.computeYearly(res[frequency.value])

        return res

   


# ------------------------------------------------------------------------------------------------------------
class ExcelFileDataSource(IDataSource):

    def __init__(self, excelFile: str):

        self.__excelFile = excelFile

    async def load(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        if frequencies is None:
            # Transform Enum in List.
            frequencyList = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequencyList = set(frequencies)

        for frequency in frequencyList:
            if frequency != Frequency.YEARLY:
                res[frequency.value] = ExcelParser.parse(self.__excelFile, frequency)
            else:
                daily = ExcelParser.parse(self.__excelFile, Frequency.DAILY)
                res[frequency.value] = FrequencyConverter.computeYearly(daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class JsonWebDataSource(WebDataSource):
    INPUT_DATE_FORMAT = "%Y-%m-%d"
    OUTPUT_DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession|None=None):

        if(session is None):
            session = aiohttp.ClientSession(cookie_jar= aiohttp.CookieJar())
        super().__init__(username, password,session)
       

    async def _loadFromSession(self,pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        computeByFrequency = {
            Frequency.HOURLY: FrequencyConverter.computeHourly,
            Frequency.DAILY: FrequencyConverter.computeDaily,
            Frequency.WEEKLY: FrequencyConverter.computeWeekly,
            Frequency.MONTHLY: FrequencyConverter.computeMonthly,
            Frequency.YEARLY: FrequencyConverter.computeYearly
        }

        # Data URL: Inject parameters.
        # Retry mechanism.
        retry = 10
        while retry > 0:


            try:
                data=await self._conso.get_consommation(pceIdentifier,startDate.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),endDate.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),ConsommationRole.INFORMATIVES)
                break
            except Exception as e:

                if retry == 1:
                    raise e

                Logger.error("An error occurred while loading data. Retry in 3 seconds.")
                time.sleep(3)
                retry -= 1

        # Temperatures URL: Inject parameters.
        endDate = date.today() - timedelta(days=1) if endDate >= date.today() else endDate
        days = min((endDate - startDate).days, 730)
        # Get weather data.
        temperatures=await self._pce.get_pce_meteo(pceIdentifier,endDate.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),days)

        # Transform all the data into the target structure.
        daily = JsonParser.parseResult(data, temperatures, pceIdentifier)

        if frequencies is None:
            # Transform Enum in List.
            frequencyList = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequencyList = set(frequencies)

        for frequency in frequencyList:
            res[frequency.value] = computeByFrequency[frequency](daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class JsonFileDataSource(IDataSource):

    def __init__(self, consumptionJsonFile: str, temperatureJsonFile):

        self.__consumptionJsonFile = consumptionJsonFile
        self.__temperatureJsonFile = temperatureJsonFile

    def load(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        with open(self.__consumptionJsonFile) as consumptionJsonFile:
            with open(self.__temperatureJsonFile) as temperatureJsonFile:
                daily = JsonParser.parse(consumptionJsonFile.read(), temperatureJsonFile.read(), pceIdentifier)

        computeByFrequency = {
            Frequency.HOURLY: FrequencyConverter.computeHourly,
            Frequency.DAILY: FrequencyConverter.computeDaily,
            Frequency.WEEKLY: FrequencyConverter.computeWeekly,
            Frequency.MONTHLY: FrequencyConverter.computeMonthly,
            Frequency.YEARLY: FrequencyConverter.computeYearly
        }

        if frequencies is None:
            # Transform Enum in List.
            frequencyList = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequencyList = set(frequencies)

        for frequency in frequencyList:
            res[frequency.value] = computeByFrequency[frequency](daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class TestDataSource(IDataSource):

    def __init__(self):

        pass

    def load(self, pceIdentifier: str, startDate: date, endDate: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        dataSampleFilenameByFrequency = {
            Frequency.HOURLY: "hourly_data_sample.json",
            Frequency.DAILY: "daily_data_sample.json",
            Frequency.WEEKLY: "weekly_data_sample.json",
            Frequency.MONTHLY: "monthly_data_sample.json",
            Frequency.YEARLY: "yearly_data_sample.json"
        }

        if frequencies is None:
            # Transform Enum in List.
            frequencyList = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequencyList = set(frequencies)

        for frequency in frequencyList:
            dataSampleFilename = f"{os.path.dirname(os.path.abspath(__file__))}/resources/{dataSampleFilenameByFrequency[frequency]}"

            with open(dataSampleFilename) as jsonFile:
                res[frequency.value] = cast(List[Dict[PropertyName, Any]], json.load(jsonFile))

        return res


