from pygazpar.enum import NatureReleve, QualificationReleve, StatusReleve
from typing import List


class Releves_type:
    def __init__(self,
                dateDebutReleve:str,
                dateFinReleve:str,
                indexDebut:int,
                indexFin:int,
                volumeBrutConsomme:float,
                energieConsomme:float,
                natureReleve:NatureReleve|str,
                qualificationReleve:QualificationReleve|str,
                journeeGaziere:str|None=None,
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

class Consommation_type:
    def __init__(self,
                 idPce:str,
                 releves:List[Releves_type],
                 frequence:str|None):
        self.idPce = idPce
        relevesArray=[]
        for element in releves:
            if not isinstance(element, Releves_type):
                relevesArray.append(Releves_type(**element))
            else:
                relevesArray.append(element)
        self.releves = relevesArray
        self.frequence = frequence

# ------------------------------------------------------------------------------------------------------------