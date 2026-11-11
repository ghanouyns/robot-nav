# maps.py - Définition de cartes / grilles de test prédéfinies

from grid import Grille
import config

def creer_grille_vide():
    """Crée une grille entièrement vide (aucun obstacle)."""
    grille = Grille(config.NB_LIGNES, config.NB_COLONNES)
    return grille

def creer_grille_mur_ouverture():
    """Crée une grille avec un grand mur vertical et une petite ouverture."""
    grille = Grille(config.NB_LIGNES, config.NB_COLONNES)
    
    # Placer un mur vertical au milieu (colonne 10) de la ligne 2 à 17
    col_mur = 10
    for ligne in range(2, 18):
        # On laisse une ouverture vers la ligne 5
        if ligne != 5:
            grille.ajouter_obstacle((ligne, col_mur))
            
    return grille

def creer_grille_labyrinthe():
    """Crée une grille avec plusieurs obstacles formant un petit labyrinthe."""
    grille = Grille(config.NB_LIGNES, config.NB_COLONNES)
    
    # Ajout de quelques murs horizontaux et verticaux en quinconce
    obstacles_coords = [
        (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
        (10, 12), (11, 12), (12, 12), (13, 12), (14, 12),
        (2, 15), (3, 15), (4, 15),
        (15, 5), (15, 6), (15, 7), (15, 8)
    ]
    
    for case in obstacles_coords:
        grille.ajouter_obstacle(case)
        
    return grille

def creer_grille_sans_solution():
    """Crée une grille où l'arrivée est totalement enfermée par un mur complet."""
    grille = Grille(config.NB_LIGNES, config.NB_COLONNES)
    
    # Entourer la position d'arrivée par un carré d'obstacles infranchissable
    # Supposons que l'arrivée par défaut est (19, 19) ou proche
    ar_l, ar_c = grille.arrivee
    
    # Mettre des obstacles tout autour de l'arrivée
    for dl in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dl != 0 or dc != 0:
                voisin_arrivee = (ar_l + dl, ar_c + dc)
                grille.ajouter_obstacle(voisin_arrivee)
                
    return grille