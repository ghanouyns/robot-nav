
import config

class Grille:
    def __init__(self, lignes=config.NB_LIGNES, colonnes=config.NB_COLONNES):
        self.lignes = lignes
        self.colonnes = colonnes

        self.obstacles = set()

        self.depart = config.DEPART_DEFAUT
        self.arrivee = config.ARRIVEE_DEFAUT

    def dans_grille(self, case):
        ligne, colonne = case

        return 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes

    def est_libre(self, case):
        return self.dans_grille(case) and case not in self.obstacles

    def ajouter_obstacle(self, case):
        if self.dans_grille(case):
            self.obstacles.add(case)

    def retirer_obstacle(self, case):
        self.obstacles.discard(case)

    def voisins(self, case):
        ligne, colonne = case

        directions = [
            (-1, 0),  
            (1, 0),   
            (0, -1),  
            (0, 1)    
        ]

        resultat = []

        for dl, dc in directions:
            nouvelle_case = (ligne + dl, colonne + dc)

            if self.est_libre(nouvelle_case):
                resultat.append(nouvelle_case)

        return resultat
