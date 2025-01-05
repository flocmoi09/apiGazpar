import json
from pygazpar.types.ConsommationType import RelevesType
from pygazpar.enum import NatureReleve, QualificationReleve, StatusReleve


class RelevesResultType(RelevesType):
    """Class representing a result consommation"""
    def __init__(self,
                time_period:str,
                timestamp:str,
                releves:RelevesType|None=None,
                temperature:str|float|None=None,
                dateDebutReleve:str|None=None,
                dateFinReleve:str|None=None,
                journeeGaziere:str|None=None,
                indexDebut:int|None=None,
                indexFin:int|None=None,
                volumeBrutConsomme:float|None=None,
                energieConsomme:float|None=None,
                pcs:str|int|float|None=None,
                volumeConverti:int|float|None=None,
                pta:str|int|float|None=None,
                natureReleve:NatureReleve|str|None=None,
                qualificationReleve:QualificationReleve|str|None=None,
                status:StatusReleve|str|None=None,
                coeffConversion:float|None=None,
                frequenceReleve:str|None=None,
                frequence:str|None=None
                 ):
        if(releves is not None ):
            if(temperature is None):
                temperature=releves.temperature
            super().__init__(dateDebutReleve=releves.dateDebutReleve,
                    dateFinReleve=releves.dateFinReleve,
                    journeeGaziere=releves.journeeGaziere,
                    indexDebut=releves.indexDebut,
                    indexFin=releves.indexFin,
                    volumeBrutConsomme=releves.volumeBrutConsomme,
                    energieConsomme=releves.energieConsomme,
                    pcs=releves.pcs,
                    volumeConverti=releves.volumeConverti,
                    pta=releves.pta,
                    natureReleve=releves.natureReleve,
                    qualificationReleve=releves.qualificationReleve,
                    status=releves.status,
                    coeffConversion=releves.coeffConversion,
                    frequenceReleve=releves.frequenceReleve,
                    temperature=temperature,
                    frequence=releves.frequence)
        else :
            super().__init__(dateDebutReleve=dateDebutReleve,
                    dateFinReleve=dateFinReleve,
                    journeeGaziere=journeeGaziere,
                    indexDebut=indexDebut,
                    indexFin=indexFin,
                    volumeBrutConsomme=volumeBrutConsomme,
                    energieConsomme=energieConsomme,
                    pcs=pcs,
                    volumeConverti=volumeConverti,
                    pta=pta,
                    natureReleve=natureReleve,
                    qualificationReleve=qualificationReleve,
                    status= status,
                    coeffConversion=coeffConversion,
                    frequenceReleve=frequenceReleve,
                    temperature=temperature,
                    frequence=frequence)

        self.time_period = time_period
        self.timestamp = timestamp
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
