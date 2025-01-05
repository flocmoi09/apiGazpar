
class ContratPce:
    """Contract class from API.

        Class represent a contract

        Attributes:
        ----------
        tarifAcheminement: str
        Ce Tarif d'acheminement gaz du titulaire est choisi par le fournisseur en fonction d'une estimation du volume de gaz consommé.
            - T1 : Consommation inférieure à 6000 kWh / an.
            - T2 : Consommation entre 6000 kWh / an et 300 MWh / an.
            - T3 : Consommation entre 300 MWh / an et 5 GWh / an (essentiellement des entreprises tertiaires ou industrielles de taille moyenne).
            - T4 : Consommation supérieure à 5 GWh / an (grands sites industriels directement rattachés au réseau de distribution de gaz naturel).
            - TP : Tarif de Proximité, il s’agit d’une option tarifaire concernant des clients finaux ayant la possibilité règlementaire de se raccorder au réseau de transport.
            - TB : Tarif Biométhane, il s'agit d'une option tarifaire concernant les producteurs de biométhane
            
        carActuelle: int
        Consommation Annuelle de Référence (CAR) en kWh :Quantité de gaz estimée consommée sur une année, dans des conditions climatiques moyennes.La CAR d’une année N s’appliquent du 1er avril de l’année N au 31 mars de l’année N+1. Elle est mise à jour de manière systématique par le Gestionnaire de Réseau de Distribution (GRD).
        carFuture: int 
        Prochaine Consommation Annuelle de Référence (CAR) en kWh
        profilTypeFutur: str
        Prochain Profil Type
        cja: str|None
        Capacité Journalière d’Acheminement (CJA) en kWh/jour :Quantité maximale d’énergie que le distributeur s'engage à acheminer chaque jour en un point de livraison.Elle se compose d’une souscription annuelle à laquelle peut s’ajouter une souscription mensuelle supplémentaire et/ou une souscription journalière supplémentaire. Ce type de donnée est applicable seulement aux compteurs JJ et pour les clients de tarif T4 ou TP (Tarif de Proximité).
        cjaMensuelle: str|None
        Souscription mensuelle supplémentaire
        cjaJournaliere: str|None
        Souscription journalière supplémentaire
        idCad: str
        nomTitulaire: str|None
        Nom du titulaire du contrat de fourniture d'énergie
        raisonSocialeTitulaire: str|None
        Raison sociale du titulaire (si applicable)
        numeroSiretTitulaire: str|None
        Numéro SIRET du titulaire (si applicable)
        dateMes: str|None
        Date de la Mise En Service (MES) du PCE correspondante au titulaire actif
        dateMhs: str|None
        Date de la Mise Hors Service (MHS) du PCE correspondante au titulaire actif
        statutContractuel: str
        Statut du contrat
        consommationJournalierePlafond: str|None
        Plafond de consommation journalière
        modulationN1: str|None
        Modulation de Stockage Année N-1
        modulationN2: str|None
        Modulation de Stockage Année N-2
        modulationN3: str|None
        Modulation de Stockage Année N-3
        modulationN4: str|None
        Modulation de Stockage Année N-4
        assiette: str|None
        Assiette de compensation de stockage. Moyenne des 2 modulation plus petite.
        fournisseur: str
        Fournisseur d'énergie souscrit
        profil: str
        Le Profil Type (est attribué par le Distributeur) caractérise la répartition de la CAR d’un PCE tout au long de l’année.
        Il est notamment utilisé entre deux relevés pour estimer les quantités journalières d'un PCE.Ce dernier est déterminé automatiquement par le système d’informations de GRDF à partir de la CAR saisie par le fournisseur (puis chaque année à partir de la CAR recalculée par GRDF).
        Dix profils types permettent de définir les usages de consommations du gaz naturel :
        - P000 : Client PCE forfait cuisine
        - P011 : Client Gazpar (compteur 1M) ou à relevé semestriel avec une CAR inférieure à 6000 kWh/an (compteur 6M)
        - P012 : Client Gazpar (compteur 1M) ou à relevé semestriel avec une CAR supérieure ou égale à 6000 kWh/an (compteur 6M)
        - P013 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne inférieure ou égale à 39%
        - P014 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne entre 39% et 50%
        - P015 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne entre 50% et 58%
        - P016 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne entre 58% et 69%
        - P017 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne entre 69% et 75%
        - P018 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne entre 75% et 81%
        - P019 : Client à relevé mensuel (compteur MM) ou journalier (compteur JJ) avec une part hiver corrigée moyenne strictement supérieure à 81%
        Le Profil Type d’une année N s’appliquent du 1er avril de l’année N au 31 mars de l’année N+1.
        Il est mis à jour de manière systématique par le Gestionnaire de Réseau de Distribution (GRD), une fois par an à date fixe, sauf en cas d'évènement spécifique :
         - Premières Mise En Service (MES)
         - Changement de fournisseur avec changement de tarif ou de fréquence de relevé
         - Changement de données tarifaires
         - Corrections d’une erreur manifeste (CAR et/ou profil aberrant)
        
        dateDebutProfil: str
        Date de début de validité du Profil Type actuel
        dateFinProfil: str
        Date de fin de validité du Profil Type actuel    

        """
    def __init__(self, 
                 tarifAcheminement:str, 
                 carActuelle:int,
                 carFuture:int,
                 profilTypeFutur:str,
                 cja:str|None,
                 cjaMensuelle:str|None,
                 cjaJournaliere:str|None,
                 idCad:str,
                 nomTitulaire:str,
                 raisonSocialeTitulaire:str,
                 numeroSiretTitulaire:str,
                 dateMes:str|None,
                 dateMhs:str|None,
                 statutContractuel:str,
                 consommationJournalierePlafond:str|None,
                 modulationN1:str|None,
                 modulationN2:str|None,
                 modulationN3:str|None,
                 modulationN4:str|None,
                 assiette: str|None,
                 fournisseur:str,
                 profil:str,
                 dateDebutProfil:str,
                dateFinProfil:str


                 ):
        self.tarifAcheminement = tarifAcheminement
        self.carActuelle = carActuelle
        self.carFuture = carFuture
        self.profilTypeFutur = profilTypeFutur
        self.cja = cja
        self.cjaMensuelle = cjaMensuelle
        self.cjaJournaliere = cjaJournaliere
        self.idCad = idCad
        self.nomTitulaire = nomTitulaire
        self.raisonSocialeTitulaire = raisonSocialeTitulaire
        self.numeroSiretTitulaire = numeroSiretTitulaire
        self.dateMes = dateMes
        self.dateMhs = dateMhs
        self.statutContractuel = statutContractuel
        self.consommationJournalierePlafond = consommationJournalierePlafond
        self.modulationN1 = modulationN1
        self.modulationN2 = modulationN2
        self.modulationN3 = modulationN3
        self.modulationN4 = modulationN4
        self.assiette = assiette
        self.fournisseur = fournisseur
        self.profil = profil
        self.dateDebutProfil = dateDebutProfil
        self.dateFinProfil = dateFinProfil
        
