# config.py - Centralisation des constantes du projet robot-nav

# --- Paramètres de la grille ---
ROWS = 20
COLS = 20
CELL_SIZE = 30  # Taille en pixels de chaque case sur le Canvas

# --- Codes couleurs de l'interface (Hexadécimal) ---
COLOR_EMPTY = "#FFFFFF"      # Blanc pour une case vide
COLOR_OBSTACLE = "#2C3E50"  # Gris foncé / Bleu nuit pour les murs
COLOR_START = "#27AE60"    # Vert pour le point de départ
COLOR_GOAL = "#C0392B"   # Rouge pour la destination
COLOR_VISITED = "#AED6F1"  # Bleu clair pour les nœuds explorés
COLOR_PATH = "#F1C40F"    # Jaune / Or pour le chemin final
COLOR_ROBOT = "#8E44AD"     # Violet pour le robot