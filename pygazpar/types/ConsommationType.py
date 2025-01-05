from typing import List
from pygazpar.enum import NatureReleve, QualificationReleve, StatusReleve


class RelevesType:
    """Class representing a Releves from API"""
    def __init__(self,
                dateDebutReleve:str,
                dateFinReleve:str,
                indexDebut:int,
                indexFin:int,
                volumeBrutConsomme:float,
                energieConsomme:float,
                natureReleve:str|NatureReleve,
                qualificationReleve:QualificationReleve|str,
                journeeGaziere:str| None=None,
                pcs:str|int|float|None=None,
                volumeConverti:int|float|None=None,
                pta:str|int|float|None=None,
                status:StatusReleve|str|None=None,
                coeffConversion:float|None=None,
                frequenceReleve:str|None=None,
                temperature:str|float|None=None,
                frequence:str|None=None):
        self.dateDebutReleve = dateDebutReleve
        self.dateFinReleve = dateFinReleve
        self.journeeGaziere = journeeGaziere
        self.indexDebut = indexDebut
        self.indexFin = indexFin
        self.volumeBrutConsomme = volumeBrutConsomme
        self.energieConsomme = energieConsomme
        self.pcs = pcs
        self.volumeConverti = volumeConverti
        self.pta = pta
        if(natureReleve is None):
            self.natureReleve = None
        else:   
            self.natureReleve =  NatureReleve(natureReleve)
        if(qualificationReleve is None):
            self.qualificationReleve = None
        else:   
            self.qualificationReleve =  QualificationReleve(qualificationReleve)
        if(status is None):
            self.status = None
        else:   
            self.status =  StatusReleve(status)
        self.coeffConversion = coeffConversion
        self.frequenceReleve = frequenceReleve
        self.temperature = temperature
        self.frequence = frequence

class ConsommationType:
    """Class representing a Result consommation send by the API"""
    def __init__(self,
                 idPce:str,
                 releves:List[RelevesType],
                 frequence:str|None):
        self.idPce = idPce
        relevesArray=[]
        for element in releves:
            if not isinstance(element, RelevesType):
                relevesArray.append(RelevesType(**element))
            else:
                relevesArray.append(element)
        self.releves = relevesArray
        self.frequence = frequence

# ------------------------------------------------------------------------------------------------------------