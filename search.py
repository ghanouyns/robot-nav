# search.py - Implémentation du BFS pour les Niveaux 1 et 2

from collections import deque


def reconstruct_path(parent, current):
    """
    Reconstruit le chemin en remontant le dictionnaire des parents,
    puis en inversant la liste.
    Le chemin renvoyé contient le départ ET l'arrivée.
    """
    path = [current]
    while current in parent:
        current = parent[current]
        path.append(current)
    path.reverse()  # Ordre : du départ vers l'arrivée
    return path


def bfs(grid, start, goal):
    """
    Algorithme BFS (Parcours en largeur).
    Utilisé pour les Niveaux 1 et 2.
    Renvoie un tuple : (chemin, nombre de cases explorées).
    Le chemin est une liste de tuples (ligne, colonne),
    ou None s'il n'y a pas de solution.
    """
    queue = deque([start])
    visited = {start}
    parent = {}
    explores_count = 0

    while queue:
        current = queue.popleft()
        explores_count += 1

        if current == goal:
            return reconstruct_path(parent, current), explores_count

        for neighbor in grid.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, explores_count