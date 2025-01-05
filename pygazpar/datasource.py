"""Support for Datasource."""
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
from pygazpar.types.PceType import PceType
Logger = logging.getLogger(__name__)

MeterReading = Dict[str, Any]

MeterReadings = List[MeterReading]

MeterReadingsByFrequency = Dict[str, MeterReadings]


# ------------------------------------------------------------------------------------------------------------
class IDataSource(ABC):
    '''Base class'''
    @abstractmethod
    async def load(self, pce_identifier: str, start_date: date, end_date: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        '''Load data conso from source'''
        pass
    @abstractmethod
    async def login(self) -> str:
        '''Login from source'''
        pass

    @abstractmethod
    async def list_pce(self) -> List[PceType]:
        '''List PCE from source'''
        pass


# ------------------------------------------------------------------------------------------------------------
class WebDataSource(IDataSource):
    '''Base class for the WEB api'''
    # ------------------------------------------------------
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):

        self.__username = username
        self.__password = password
        self.__session = session
        self._pce= GazparPCE(session)
        self._conso=GazparConsommation(session)
        self._auth=GazparAuth(username, password,session)
        self._auth_token=None
    async def login(self) -> str:
         self._auth_token=await self._auth.request_token()
         return self._auth_token
    async def list_pce(self) -> List[PceType]:
         return await self._pce.get_list_pce()
    # ------------------------------------------------------
    async def load(self, pce_identifier: str, start_date: date, end_date: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        if(self._auth_token is None):
            self._auth_token=await self._auth.request_token()
        
        res = await self._load_from_session(pce_identifier, start_date, end_date, frequencies)

        Logger.debug("The data update terminates normally")

        return res


    @abstractmethod
    async def _load_from_session(self, pce_identifier: str, start_date: date, end_date: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        '''Load data from session'''
        pass


# ------------------------------------------------------------------------------------------------------------
class ExcelWebDataSource(WebDataSource):
    '''Base class for the Excel WEB api'''

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

        if session is None:
            session = aiohttp.ClientSession(cookie_jar= aiohttp.CookieJar())
      
        super().__init__(username, password,session)
        
        self.__tmp_directory = tmpDirectory
    
    # ------------------------------------------------------
    async def _load_from_session(self, pce_identifier: str, start_date: date, end_date: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        # XLSX is in the TMP directory
        data_file_path_pattern = self.__tmp_directory + '/' + ExcelWebDataSource.DATA_FILENAME

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
            frequency_list = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequency_list = set(frequencies)

        for frequency in frequency_list:
            # Inject parameters.

            Logger.debug(f"Loading data of frequency {ExcelWebDataSource.FREQUENCY_VALUES[frequency]} from {start_date.strftime(ExcelWebDataSource.DATE_FORMAT)} to {end_date.strftime(ExcelWebDataSource.DATE_FORMAT)}")

            # Retry mechanism.
            retry = 10
            while retry > 0:


                try:
                    response = await self._conso.get_consommation_file(pce_identifier,start_date.strftime(ExcelWebDataSource.DATE_FORMAT),end_date.strftime(ExcelWebDataSource.DATE_FORMAT),ConsommationRole.INFORMATIVES,frequency)
                    open(f"{self.__tmp_directory}/{response.filename}", "wb").write(response.content)

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
                Logger.warning(f"Not any data file has been found in '{self.__tmp_directory}' directory")

            for filename in file_list:
                res[frequency.value] = ExcelParser.parse(filename, frequency if frequency != Frequency.YEARLY else Frequency.DAILY)
                try:
                    # openpyxl does not close the file properly.
                    os.remove(filename)
                except PermissionError:
                    pass

            # We compute yearly from daily data.
            if frequency == Frequency.YEARLY:
                res[frequency.value] = FrequencyConverter.compute_yearly(res[frequency.value])

        return res

   


# ------------------------------------------------------------------------------------------------------------
class ExcelFileDataSource(IDataSource):
    '''Base class for the Excel file'''
    def __init__(self, excel_file: str):

        self.__excel_file = excel_file
    async def login(self) -> str:
         pass
    async def list_pce(self) -> List[PceType]:
        '''List PCE from source'''
        pass
    async def load(self, pce_identifier: str, start_date: date,
                   end_date: date, frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        if frequencies is None:
            # Transform Enum in List.
            frequency_list = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequency_list = set(frequencies)

        for frequency in frequency_list:
            if frequency != Frequency.YEARLY:
                res[frequency.value] = ExcelParser.parse(self.__excel_file, frequency)
            else:
                daily = ExcelParser.parse(self.__excel_file, Frequency.DAILY)
                res[frequency.value] = FrequencyConverter.compute_yearly(daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class JsonWebDataSource(WebDataSource):
    '''Base class for the Json Web data'''
    INPUT_DATE_FORMAT = "%Y-%m-%d"
    OUTPUT_DATE_FORMAT = "%d/%m/%Y"

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession|None=None):

        if session is None:
            session = aiohttp.ClientSession(cookie_jar= aiohttp.CookieJar())
        super().__init__(username, password,session)

    async def _load_from_session(self,pce_identifier: str, start_date: date, end_date: date, 
                                 frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        compute_by_frequency = {
            Frequency.HOURLY: FrequencyConverter.compute_hourly,
            Frequency.DAILY: FrequencyConverter.compute_daily,
            Frequency.WEEKLY: FrequencyConverter.compute_weekly,
            Frequency.MONTHLY: FrequencyConverter.compute_monthly,
            Frequency.YEARLY: FrequencyConverter.compute_yearly
        }

        # Data URL: Inject parameters.
        # Retry mechanism.
        retry = 10
        while retry > 0:


            try:
                data=await self._conso.get_consommation(pce_identifier,start_date.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),
                                                        end_date.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),ConsommationRole.INFORMATIVES)
                break
            except Exception as e:

                if retry == 1:
                    raise e

                Logger.error("An error occurred while loading data. Retry in 3 seconds.")
                time.sleep(3)
                retry -= 1

        # Temperatures URL: Inject parameters.
        end_date = date.today() - timedelta(days=1) if end_date >= date.today() else end_date
        days = min((end_date - start_date).days, 730)
        # Get weather data.
        temperatures=await self._pce.get_pce_meteo(pce_identifier,end_date.strftime(JsonWebDataSource.INPUT_DATE_FORMAT),days)

        # Transform all the data into the target structure.
        daily = JsonParser.parse_result(data, temperatures, pce_identifier)

        if frequencies is None:
            # Transform Enum in List.
            frequency_list = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequency_list = set(frequencies)

        for frequency in frequency_list:
            res[frequency.value] = compute_by_frequency[frequency](daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class JsonFileDataSource(IDataSource):
    '''Base class for the Json File data'''
    def __init__(self, consumption_json_file: str, temperature_json_file):

        self.__consumption_json_file = consumption_json_file
        self.__temperature_json_file = temperature_json_file
    async def login(self) -> str:
         pass
    async def list_pce(self) -> List[PceType]:
        '''List PCE from source'''
        pass
    async def load(self, pce_identifier: str, start_date: date, end_date: date,
                   frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}

        with open(self.__consumption_json_file) as __consumption_json_file:
            with open(self.__temperature_json_file) as __temperature_json_file:
                daily = JsonParser.parse(__consumption_json_file.read(), __temperature_json_file.read(), pce_identifier)

        compute_by_frequency = {
            Frequency.HOURLY: FrequencyConverter.compute_hourly,
            Frequency.DAILY: FrequencyConverter.compute_daily,
            Frequency.WEEKLY: FrequencyConverter.compute_weekly,
            Frequency.MONTHLY: FrequencyConverter.compute_monthly,
            Frequency.YEARLY: FrequencyConverter.compute_yearly
        }

        if frequencies is None:
            # Transform Enum in List.
            frequency_list = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequency_list = set(frequencies)

        for frequency in frequency_list:
            res[frequency.value] = compute_by_frequency[frequency](daily)

        return res


# ------------------------------------------------------------------------------------------------------------
class TestDataSource(IDataSource):
    '''Base class for the Test data'''
    def __init__(self):
        pass
    async def login(self) -> str:
         pass
    async def list_pce(self) -> List[PceType]:
        '''List PCE from source'''
        pass
    async def load(self, pce_identifier: str, start_date: date, end_date: date,
                   frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:

        res = {}
        data_sample_filename_by_frequency = {
            Frequency.HOURLY: "hourly_data_sample.json",
            Frequency.DAILY: "daily_data_sample.json",
            Frequency.WEEKLY: "weekly_data_sample.json",
            Frequency.MONTHLY: "monthly_data_sample.json",
            Frequency.YEARLY: "yearly_data_sample.json"
        }

        if frequencies is None:
            # Transform Enum in List.
            frequency_list = [frequency for frequency in Frequency]
        else:
            # Get unique values.
            frequency_list = set(frequencies)

        for frequency in frequency_list:
            data_sample_filename = f"{os.path.dirname(os.path.abspath(__file__))}/resources/{data_sample_filename_by_frequency[frequency]}"

            with open(data_sample_filename) as json_file:
                res[frequency.value] = cast(List[Dict[PropertyName, Any]], json.load(json_file))

        return res
