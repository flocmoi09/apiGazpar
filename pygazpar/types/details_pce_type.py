
from .contrat_type import contrat_pce

class technique_pce:
    def __init__(self, 
                 calibre:str|None, 
                 numeroMatricule:str,
                 codeDebit:str,
                 frequence:str,
                 idPitd:str,
                 libellePitd:str,
                 clientSensibleMig:str,
                 proprieteCompteur:str,
                 proprieteDetendeur:str|None,
                 convertisseur:str|None,
                 proprieteEnregistreur:str|None,
                 roues:int,
                 debit:str,
                 pressionAval:str|None,
                 numeroRue:str|None,
                 nomRue:str|None,
                 complementAdresse:str|None,
                 codePostal:str|None,
                 codeInseeCommune:str|None,
                 commune:str|None,
                 situationCompteur:str|None,
                 accessibiliteCompteur:str|None,
                 reperageRobinetGaz:str|None,
                 numeroSerie:str|None,
                 etatCompteur:str|None,
                 codeEtatTechniquePce:str|None,
                 libelleEtatTechniquePce:str|None,
                 telereleve:bool,
                 codeEtatCommunication: str|None,
                 libelleEtatCommunication:str|None,
                 codeNatureGaz:str|None,
                 libelleNatureGaz: str|None,

                 ):
        self.calibre = calibre
        self.numeroMatricule = numeroMatricule
        self.codeDebit = codeDebit
        self.frequence = frequence
        self.idPitd = idPitd
        self.libellePitd = libellePitd
        self.clientSensibleMig = clientSensibleMig
        self.proprieteCompteur = proprieteCompteur
        self.proprieteDetendeur = proprieteDetendeur
        self.convertisseur = convertisseur
        self.proprieteEnregistreur = proprieteEnregistreur
        self.roues = roues
        self.debit = debit
        self.pressionAval = pressionAval
        self.numeroRue = numeroRue
        self.nomRue = nomRue
        self.complementAdresse = complementAdresse
        self.codePostal = codePostal
        self.codeInseeCommune = codeInseeCommune    
        self.commune = commune
        self.situationCompteur = situationCompteur
        self.accessibiliteCompteur = accessibiliteCompteur
        self.reperageRobinetGaz = reperageRobinetGaz
        self.numeroSerie = numeroSerie
        self.etatCompteur = etatCompteur
        self.codeEtatTechniquePce = codeEtatTechniquePce
        self.libelleEtatTechniquePce = libelleEtatTechniquePce
        self.telereleve = telereleve
        self.codeEtatCommunication = codeEtatCommunication
        self.libelleEtatCommunication = libelleEtatCommunication
        self.codeNatureGaz = codeNatureGaz
        self.libelleNatureGaz = libelleNatureGaz

class details_pce:
    def __init__(self, 
                 technique:technique_pce, 
                 contrat:contrat_pce,
                 statutRestitutionTechnique:str|None,
                 statutRestitutionContrat:str|None,
                 
                 ):
        if not isinstance(technique, technique_pce) and isinstance(technique, dict):
            self.technique=technique_pce(**technique)
        else:
            self.technique = technique
        if not isinstance(contrat, contrat_pce) and isinstance(contrat, dict):
            self.contrat=contrat_pce(**contrat)
        else:
            self.contrat = contrat
        self.statutRestitutionTechnique = statutRestitutionTechnique
        self.statutRestitutionContrat = statutRestitutionContrat