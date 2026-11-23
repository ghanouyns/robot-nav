
import tkinter as tk
import config

from grid import Grille
from search import bfs


class Application:

    def __init__(self):

        # ==============================
        # 1. Créer la grille
        # ==============================

        self.grille = Grille()

        # Variables pour stocker le chemin et les mesures
        self.chemin = None
        self.nb_explores = 0
        self.longueur_chemin = 0

        # ==============================
        # 2. Créer la fenêtre
        # ==============================

        self.fenetre = tk.Tk()
        self.fenetre.title(config.TITRE_FENETRE)

        # ==============================
        # 3. Créer le Canvas
        # ==============================

        largeur = (
            config.NB_COLONNES * config.TAILLE_CASE
            + 2 * config.MARGE
        )

        hauteur = (
            config.NB_LIGNES * config.TAILLE_CASE
            + 2 * config.MARGE
        )

        self.canvas = tk.Canvas(
            self.fenetre,
            width=largeur,
            height=hauteur,
            bg=config.COULEUR_FOND
        )

        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # ==============================
        # 4. Créer le panneau de boutons
        # ==============================

        self.panneau = tk.Frame(
            self.fenetre,
            width=config.LARGEUR_PANNEAU
        )

        self.panneau.pack(
            side=tk.RIGHT,
            fill=tk.Y,
            padx=10,
            pady=10
        )

        # Empêcher le panneau de changer automatiquement de largeur
        self.panneau.pack_propagate(False)

        # Bouton Lancer
        bouton_lancer = tk.Button(
            self.panneau,
            text="Lancer",
            command=self.lancer
        )

        bouton_lancer.pack(fill=tk.X, pady=5)

        # Bouton Réinitialiser
        bouton_reset = tk.Button(
            self.panneau,
            text="Réinitialiser",
            command=self.reinitialiser
        )

        bouton_reset.pack(fill=tk.X, pady=5)
        
        # Bouton Générer des obstacles
        bouton_aleatoire = tk.Button(
            self.panneau,
            text="Générer obstacles",
            command=self.generer_obstacles
        )

        bouton_aleatoire.pack(fill=tk.X, pady=5)

        # ==============================
        # 5. Affichage des mesures
        # ==============================

        self.label_explores = tk.Label(
            self.panneau,
            text="Cases explorées : 0"
        )

        self.label_explores.pack(pady=10)

        self.label_longueur = tk.Label(
            self.panneau,
            text="Longueur du chemin : 0"
        )

        self.label_longueur.pack(pady=5)

        self.label_resultat = tk.Label(
            self.panneau,
            text="En attente..."
        )

        self.label_resultat.pack(pady=10)

        # ==============================
        # 6. Gérer les clics de souris
        # ==============================

        self.canvas.bind(
            "<Button-1>",
            self.au_clic
        )

        # Premier dessin
        self.dessiner()

    # ==========================================
    # Convertir les pixels en coordonnées de case
    # ==========================================

    def case_depuis_pixels(self, x, y):

        # Vérifier si le clic est dans la grille
        if x < config.MARGE or y < config.MARGE:
            return None

        if x >= config.MARGE + self.grille.colonnes * config.TAILLE_CASE:
            return None

        if y >= config.MARGE + self.grille.lignes * config.TAILLE_CASE:
            return None

        # Convertir les pixels en ligne et colonne
        colonne = (x - config.MARGE) // config.TAILLE_CASE
        ligne = (y - config.MARGE) // config.TAILLE_CASE

        return (ligne, colonne)

    # ==========================================
    # Gérer le clic de souris
    # ==========================================

    def au_clic(self, event):

        case = self.case_depuis_pixels(event.x, event.y)

        # Ignorer les clics hors de la grille
        if case is None:
            return

        # Ne pas modifier le départ ou l'arrivée
        if case == self.grille.depart or case == self.grille.arrivee:
            return

        # Si la case contient déjà un obstacle, le retirer
        if case in self.grille.obstacles:
            self.grille.retirer_obstacle(case)

        # Sinon, ajouter un obstacle
        else:
            self.grille.ajouter_obstacle(case)

        # Effacer l'ancien chemin
        self.chemin = None
        self.nb_explores = 0
        self.longueur_chemin = 0

        # Réinitialiser le message
        self.label_resultat.config(
            text="En attente..."
        )

        # Mettre à jour les mesures
        self.mettre_a_jour_mesures()

        # Redessiner la grille
        self.dessiner()

    # ==========================================
    # Lancer l'algorithme BFS
    # ==========================================

    def lancer(self):

        self.chemin, self.nb_explores = bfs(
            self.grille,
            self.grille.depart,
            self.grille.arrivee
        )

        # Calculer la longueur du chemin
        if self.chemin is not None:

            self.longueur_chemin = len(self.chemin) - 1

            self.label_resultat.config(
                text="Chemin trouvé !"
            )

        else:

            self.longueur_chemin = 0

            self.label_resultat.config(
                text="Aucun chemin trouvé !"
            )

        # Actualiser les mesures
        self.mettre_a_jour_mesures()

        # Dessiner le chemin
        self.dessiner()

    # ==========================================
    # Réinitialiser la grille
    # ==========================================

    def reinitialiser(self):

        # Supprimer tous les obstacles
        self.grille.obstacles.clear()

        # Supprimer le chemin
        self.chemin = None

        # Réinitialiser les mesures
        self.nb_explores = 0
        self.longueur_chemin = 0

        self.label_resultat.config(
            text="En attente..."
        )

        self.mettre_a_jour_mesures()

        self.dessiner()

    # ==========================================
    # Actualiser les mesures
    # ==========================================

    def mettre_a_jour_mesures(self):

        self.label_explores.config(
            text=f"Cases explorées : {self.nb_explores}"
        )

        self.label_longueur.config(
            text=f"Longueur du chemin : {self.longueur_chemin}"
        )

    # ==========================================
    # Dessiner un point (départ ou arrivée)
    # ==========================================

    def dessiner_point(self, case, couleur):

        ligne, colonne = case

        x1 = config.MARGE + colonne * config.TAILLE_CASE
        y1 = config.MARGE + ligne * config.TAILLE_CASE

        x2 = x1 + config.TAILLE_CASE
        y2 = y1 + config.TAILLE_CASE

        self.canvas.create_oval(
            x1 + 5,
            y1 + 5,
            x2 - 5,
            y2 - 5,
            fill=couleur,
            outline=couleur
        )

    # ==========================================
    # Dessiner toute la grille
    # ==========================================

    def dessiner(self):

        # Effacer tout le Canvas
        self.canvas.delete("all")

        # Dessiner les cases
        for ligne in range(self.grille.lignes):

            for colonne in range(self.grille.colonnes):

                x1 = config.MARGE + colonne * config.TAILLE_CASE
                y1 = config.MARGE + ligne * config.TAILLE_CASE

                x2 = x1 + config.TAILLE_CASE
                y2 = y1 + config.TAILLE_CASE

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline=config.COULEUR_LIGNES
                )

        # Dessiner les obstacles
        for ligne, colonne in self.grille.obstacles:

            x1 = config.MARGE + colonne * config.TAILLE_CASE
            y1 = config.MARGE + ligne * config.TAILLE_CASE

            x2 = x1 + config.TAILLE_CASE
            y2 = y1 + config.TAILLE_CASE

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=config.COULEUR_OBSTACLE,
                outline=config.COULEUR_OBSTACLE
            )

        # Dessiner le chemin
        if self.chemin is not None and len(self.chemin) > 1:

            points = []

            for ligne, colonne in self.chemin:

                x = (
                    config.MARGE
                    + colonne * config.TAILLE_CASE
                    + config.TAILLE_CASE // 2
                )

                y = (
                    config.MARGE
                    + ligne * config.TAILLE_CASE
                    + config.TAILLE_CASE // 2
                )

                points.extend([x, y])

            self.canvas.create_line(
                *points,
                fill=config.COULEUR_CHEMIN,
                width=config.EPAISSEUR_CHEMIN
            )

        # Dessiner le départ
        self.dessiner_point(
            self.grille.depart,
            config.COULEUR_ROBOT
        )

        # Dessiner l'arrivée
        self.dessiner_point(
            self.grille.arrivee,
            config.COULEUR_ARRIVEE
        )
    # ==========================================
    # Générer des obstacles aléatoires
    # ==========================================

    def generer_obstacles(self):

        # Générer les obstacles dans la grille
        self.grille.generer_obstacles_aleatoires()

        # Supprimer l'ancien chemin
        self.chemin = None

        # Réinitialiser les mesures
        self.nb_explores = 0
        self.longueur_chemin = 0

        # Réinitialiser le message
        self.label_resultat.config(
            text="Obstacles générés !"
        )

        # Actualiser les mesures
        self.mettre_a_jour_mesures()

        # Redessiner la grille
        self.dessiner()

    # ==========================================
    # Lancer l'interface
    # ==========================================

    def lancer_interface(self):

        self.fenetre.mainloop()
