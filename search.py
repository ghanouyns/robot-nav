
from collections import deque


# ==================================================
# Reconstruction du chemin
# ==================================================

def reconstruct(parent, depart, arrivee):
    """
    Reconstruit le chemin entre le départ et l'arrivée
    en utilisant le dictionnaire parent.
    """

    chemin = []
    courant = arrivee

    while courant is not None:
        chemin.append(courant)
        courant = parent[courant]

    chemin.reverse()

    return chemin


# ==================================================
# BFS : Breadth-First Search
# ==================================================

def bfs(grille, depart, arrivee):
    """
    Recherche un chemin avec l'algorithme BFS.

    Paramètres :
        grille  : objet Grille
        depart  : tuple (ligne, colonne)
        arrivee : tuple (ligne, colonne)

    Retour :
        (chemin, nb_explores) si un chemin existe.
        (None, nb_explores) sinon.
    """

    # Vérifier que le départ et l'arrivée sont libres
    if not grille.est_libre(depart) or not grille.est_libre(arrivee):
        return None, 0

    # Initialiser la file FIFO
    file = deque([depart])

    # Ensemble des cases déjà visitées
    visites = {depart}

    # Dictionnaire pour mémoriser les parents
    parent = {depart: None}

    # Compteur des cases explorées
    nb_explores = 0

    # Parcours de la grille
    while file:

        # Récupérer la première case de la file
        courant = file.popleft()

        # Incrémenter le nombre de cases explorées
        nb_explores += 1

        # Vérifier si on a atteint l'arrivée
        if courant == arrivee:
            chemin = reconstruct(parent, depart, arrivee)
            return chemin, nb_explores

        # Parcourir les voisins de la case actuelle
        for voisin in grille.voisins(courant):

            # Vérifier si le voisin n'a pas déjà été visité
            if voisin not in visites:

                # Marquer le voisin comme visité
                visites.add(voisin)

                # Mémoriser son parent
                parent[voisin] = courant

                # Ajouter le voisin à la fin de la file
                file.append(voisin)

    # Aucun chemin trouvé
    return None, nb_explores
