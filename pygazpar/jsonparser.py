import json
import logging
from typing import Any, List, Dict
from datetime import datetime
from pygazpar.enum import PropertyName
from pygazpar.types.ConsommationType import ConsommationType
from pygazpar.types.RelevesResultType import RelevesResultType

INPUT_DATE_FORMAT = "%Y-%m-%d"

OUTPUT_DATE_FORMAT = "%d/%m/%Y"

Logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------------------
class JsonParser:

    # ------------------------------------------------------
    @staticmethod
    def parseResult(data: ConsommationType, temperatures: Dict[str, Any], pceIdentifier: str) -> List[RelevesResultType]:

        res = []



        # Timestamp of the data.
        data_timestamp = datetime.now().isoformat()

        for releve in data.releves:
            temperature = releve.temperature
            if temperature is None and temperatures is not None and len(temperatures) > 0:
                temperature = temperatures.get(releve.journeeGaziere)
            item = RelevesResultType(datetime.strftime(datetime.strptime(releve.journeeGaziere, INPUT_DATE_FORMAT), OUTPUT_DATE_FORMAT),data_timestamp,releve,temperature)
            res.append(item)

        Logger.debug("Daily data read successfully from Json")

        return res
 # ------------------------------------------------------
    @staticmethod
    def parse(jsonStr: str, temperaturesStr: str, pceIdentifier: str) -> List[Dict[str, Any]]:    
        res = []
        data = json.loads(jsonStr)

        temperatures = json.loads(temperaturesStr)

        # Timestamp of the data.
        data_timestamp = datetime.now().isoformat()

        for releve in data[pceIdentifier]['releves']:
            temperature = releve['temperature']
            if temperature is None and temperatures is not None and len(temperatures) > 0:
                releve.temperature = temperatures.get(releve['journeeGaziere'])

            item = {}
            item[PropertyName.TIME_PERIOD.value] = datetime.strftime(datetime.strptime(releve['journeeGaziere'], INPUT_DATE_FORMAT), OUTPUT_DATE_FORMAT)
            item[PropertyName.START_INDEX.value] = releve['indexDebut']
            item[PropertyName.END_INDEX.value] = releve['indexFin']
            item[PropertyName.VOLUME.value] = releve['volumeBrutConsomme']
            item[PropertyName.ENERGY.value] = releve['energieConsomme']
            item[PropertyName.CONVERTER_FACTOR.value] = releve['coeffConversion']
            item[PropertyName.TEMPERATURE.value] = temperature
            item[PropertyName.QUALIFICATION.value] = releve['qualificationReleve']
            item[PropertyName.TIMESTAMP.value] = data_timestamp

            res.append(item)

        Logger.debug("Daily data read successfully from Json")

        return res