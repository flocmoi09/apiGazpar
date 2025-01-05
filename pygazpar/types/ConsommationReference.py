class ConsommationReference:
    """Class representing a reference consommation from API"""
    def __init__(self,
                 id:int,
                 consommationType:str,
                 profile:str,
                 annee:int,
                 mois1:str,
                 mois2:str,
                 mois3:str,
                 mois4:str,
                 mois5:str,
                 mois6:str,
                 mois7:str,
                 mois8:str,
                 mois9:str,
                 mois10:str,
                 mois11:str,
                 mois12:str,
                 unite:str):
        self.id = id
        self.consommationType = consommationType
        self.profile = profile
        self.annee = annee
        self.mois1 = mois1
        self.mois2 = mois2
        self.mois3 = mois3
        self.mois4 = mois4
        self.mois5 = mois5
        self.mois6 = mois6
        self.mois7 = mois7
        self.mois8 = mois8
        self.mois9 = mois9
        self.mois10 = mois10
        self.mois11 = mois11
        self.mois12 = mois12
        self.unite = unite
    