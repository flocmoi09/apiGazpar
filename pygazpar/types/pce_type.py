from .details_pce_type import details_pce
from .contrat_type import contrat_pce
class pce_type:
    def __init__(self, 
                idObject:str, 
                typeObject:str|None,
                role:str,
                alias:str,
                teleReleve:bool,
                pce:str,
                dateActivation:str,
                dateMhs:str|None,
                dateMes:str|None,
                codePostal:str,
                frequenceReleve:str,
                etat:str,
                datePremiereAccreditation:str,
                nomTitulaire:str,
                 idAccreditation:str|None,
                raisonSociale:str|None,
                denominationClient:str|None,
                adresseEmailClient:str|None,
                telephoneClient:str|None,
                dateCreation:str|None,
                dateDebutConsentement:str|None,
                dateFinConsentement:str|None,
                dateDebutAccesDonneesConso:str|None,
                dateFinAccesDonneesConso:str|None,
                dateEtat:str|None,
                donneesConsoPubliees:str|None,
                donneesConsoInformatives:str|None,
                donneesContractuelles:str|None,
                donneesTechniques:str|None,
                parcours: str|None,
                statutControlePreuves:str|None,
                dateLimitePreuves:str|None,
                details:details_pce|None,
                dateDerniereVerification:str,
                frequenceJJ:bool = None,
                frequence1:bool =None,
                frequenceMM:bool =None,
                frequence6M:bool =None,
                frequenceMMOrJJ:bool =None,
                numeroSerie:str =None,
                numeroMatricule:str =None,
                contrat:contrat_pce=None,
                fullAddress:str=None,
                **kwargs
                 ):
        self.idObject = idObject
        self.typeObject = typeObject
        self.idAccreditation = idAccreditation
        self.raisonSociale = raisonSociale
        self.denominationClient = denominationClient
        self.adresseEmailClient = adresseEmailClient
        self.telephoneClient = telephoneClient
        self.dateCreation = dateCreation
        self.dateDebutConsentement = dateDebutConsentement
        self.dateFinConsentement = dateFinConsentement
        self.dateDebutAccesDonneesConso = dateDebutAccesDonneesConso
        self.dateFinAccesDonneesConso = dateFinAccesDonneesConso
        self.dateEtat = dateEtat
        self.donneesConsoPubliees = donneesConsoPubliees
        self.donneesConsoInformatives = donneesConsoInformatives
        self.donneesContractuelles = donneesContractuelles
        self.donneesTechniques = donneesTechniques
        self.parcours = parcours
        self.statutControlePreuves = statutControlePreuves
        self.dateLimitePreuves = dateLimitePreuves
        self.role =role
        self.alias = alias
        self.teleReleve = teleReleve
        self.pce = pce
        self.dateActivation = dateActivation
        self.dateMhs = dateMhs
        self.dateMes = dateMes
        self.codePostal = codePostal
        self.frequenceReleve = frequenceReleve
        self.etat = etat
        self.datePremiereAccreditation = datePremiereAccreditation
        self.nomTitulaire = nomTitulaire
        if not isinstance(details, details_pce) and isinstance(details, dict):
            self.details=details_pce(**details)
        else:
            self.details = details
      
        self.dateDerniereVerification = dateDerniereVerification
        self.frequenceJJ = frequenceJJ
        self.frequence1 = frequence1
        self.frequenceMM = frequenceMM
        self.frequence6M = frequence6M
        self.frequenceMMOrJJ = frequenceMMOrJJ
        self.numeroSerie = numeroSerie
        self.numeroMatricule = numeroMatricule
        if not isinstance(contrat, contrat_pce) and isinstance(contrat, dict):
            self.contrat=contrat_pce(**contrat)
        else:
            self.contrat = contrat
        
        self.fullAddress = fullAddress