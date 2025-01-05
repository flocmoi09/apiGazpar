"""Support for Enum."""
from enum import Enum


# ------------------------------------------------------------------------------------------------------------
class PropertyName(Enum):
    '''Get the name of the field'''
    TIME_PERIOD = "time_period"
    DATE_DEBUT = "dateDebutReleve"
    DATE_FIN = "dateFinReleve"

    JOURNEE_GAZIERE = "journeeGaziere"
    START_INDEX = "indexDebut"
    END_INDEX = "indexFin"
    VOLUME = "volumeBrutConsomme"
    ENERGY = "energieConsomme"
    PCS = "pcs"
    VOLUME_CONVERTI = "volumeConverti"
    PTA = "pta"
    NATURE = "natureReleve"
    QUALIFICATION = "qualificationReleve"
    STATUS = "status"
    FREQUENCE_RELEVE= "frequenceReleve"
    CONVERTER_FACTOR = "coeffConversion"
    TEMPERATURE = "temperature"
    FREQUENCE= "frequence"
    TIMESTAMP = "timestamp"                
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()


# ------------------------------------------------------------------------------------------------------------
class Frequency(Enum):
    '''Get frequency'''
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()
class ConsommationRole(str,Enum):
    '''Get type conso for API'''
    INFORMATIVES = 'informatives'
    PUBLIEES = 'publiees'
class NatureReleve(str,Enum):
    '''Get nature type for releve'''
    PUBLIEES = 'Publiée'
    INFORMATIVES = 'Informative Journalier'
class QualificationReleve(str,Enum):
    '''Get qualification type for releve'''
    ESTIME='Estimé'
    CORRIGE='Corrigé'
    MESURE='Mesuré'
    ABSENT='Absence de Données'
class StatusReleve(str,Enum):
    '''Get status type for releve'''
    PROVISOIRE='Provisoire'
    DEFINITIVE='Définitive'
