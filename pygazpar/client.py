"""Support for API Methods."""
from typing import List, Optional
import logging
from datetime import date, timedelta
from pygazpar.enum import Frequency
from pygazpar.datasource import IDataSource, MeterReadingsByFrequency

DEFAULT_LAST_N_DAYS = 365
Logger = logging.getLogger(__name__)


# ---------------------------------------------------------
class Client:
    '''Get the API Client'''
    # ------------------------------------------------------
    def __init__(self, datasource: IDataSource):
        self.__datasource = datasource

    # ------------------------------------------------------
    async def load_since(self, pce_identifier: str, last_n_days: int = DEFAULT_LAST_N_DAYS,
                        frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        '''Load data since last N days'''
        try:
            end_date = date.today()
            start_date = end_date + timedelta(days=-last_n_days)
            res = await self.load_date_range(pce_identifier, start_date, end_date, frequencies)
        except Exception:
            Logger.error("An unexpected error occured while loading the data", exc_info=True)
            raise

        return res

    # ------------------------------------------------------
    async def load_date_range(self, pce_identifier: str, start_date: date, end_date: date,
                            frequencies: Optional[List[Frequency]] = None) -> MeterReadingsByFrequency:
        '''Load data since two date'''
        Logger.debug("Start loading the data...")
        try:
            res = await self.__datasource.load(pce_identifier, start_date, end_date, frequencies)
            Logger.debug("The data load terminates normally")
        except Exception:
            Logger.error("An unexpected error occured while loading the data", exc_info=True)
            raise

        return res
