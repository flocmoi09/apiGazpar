from enum import Enum


# ------------------------------------------------------------------------------------------------------------
class PropertyName(Enum):
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
    INFORMATIVES = 'informatives'
    PUBLIEES = 'publiees'
class NatureReleve(str,Enum):
    PUBLIEES = 'Publiée'
    INFORMATIVES = 'Informative Journalier'
class QualificationReleve(str,Enum):
    ESTIME='Estimé'
    CORRIGE='Corrigé'
    MESURE='Mesuré'
    ABSENT='Absence de Données'
class StatusReleve(str,Enum):
    PROVISOIRE='Provisoire'
    DEFINITIVE='Définitive'