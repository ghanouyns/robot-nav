# ui.py - Interface graphique finale avec placement manuel du Départ et de l'Arrivée

import tkinter as tk
import random
import config
from grid import Grille
from search import bfs

class RobotNavApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.TITRE_FENETRE)

        # Initialisation de la grille standard
        self.grille = Grille(config.NB_LIGNES, config.NB_COLONNES)

        # Variables d'état
        self.chemin = []
        self.nb_explores = 0
        self.simulation_active = False
        
        # Mode de placement au clic : "depart", "arrivee", ou "obstacle"
        self.mode_placement = "obstacle"

        # Création des éléments de l'interface
        self.create_widgets()
        self.dessiner_grille()

    def create_widgets(self):
        """Crée le panneau de contrôle et le Canvas."""
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # --- Boutons d'actions principaux ---
        btn_run = tk.Button(control_frame, text="Lancer BFS", command=self.executer_bfs, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
        btn_run.pack(side=tk.LEFT, padx=3)

        # Bouton unique pour Activer ou Stopper le mode dynamique
        self.btn_dynamique = tk.Button(control_frame, text="Activer Dynamique", command=self.basculer_dynamique, bg="#FF9800", fg="white", font=("Arial", 9, "bold"))
        self.btn_dynamique.pack(side=tk.LEFT, padx=3)

        # --- Boutons pour choisir quoi placer au clic ---
        self.btn_mode_depart = tk.Button(control_frame, text="Placer Départ", command=lambda: self.changer_mode("depart"), bg="#2196F3", fg="white", font=("Arial", 9, "bold"))
        self.btn_mode_depart.pack(side=tk.LEFT, padx=3)

        self.btn_mode_arrivee = tk.Button(control_frame, text="Placer Arrivée", command=lambda: self.changer_mode("arrivee"), bg="#9C27B0", fg="white", font=("Arial", 9, "bold"))
        self.btn_mode_arrivee.pack(side=tk.LEFT, padx=3)

        btn_clear = tk.Button(control_frame, text="Effacer", command=self.reinitialiser_grille, bg="#f44336", fg="white", font=("Arial", 9, "bold"))
        btn_clear.pack(side=tk.LEFT, padx=3)

        # --- Label d'information ---
        self.label_info = tk.Label(self.root, text="Mode actuel : Obstacles (Cliquez pour ajouter/retirer).", font=("Arial", 9))
        self.label_info.pack(side=tk.TOP, pady=5)

        # --- Canvas pour la grille ---
        canvas_width = self.grille.colonnes * config.TAILLE_CASE
        canvas_height = self.grille.lignes * config.TAILLE_CASE
        
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg=config.COULEUR_FOND)
        self.canvas.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.sur_clic_canvas)

    def changer_mode(self, mode):
        """Change ce que l'utilisateur va placer au prochain clic."""
        self.mode_placement = mode
        if mode == "depart":
            self.label_info.config(text="📍 Cliquez sur la grille pour placer le nouveau Départ.")
        elif mode == "arrivee":
            self.label_info.config(text="🏁 Cliquez sur la grille pour placer la nouvelle Arrivée.")

    def dessiner_grille(self):
        """Dessine les cases de la grille."""
        self.canvas.delete("all")

        for r in range(self.grille.lignes):
            for c in range(self.grille.colonnes):
                x1 = c * config.TAILLE_CASE
                y1 = r * config.TAILLE_CASE
                x2 = x1 + config.TAILLE_CASE
                y2 = y1 + config.TAILLE_CASE

                pos = (r, c)
                couleur = config.COULEUR_FOND

                if pos == self.grille.depart:
                    couleur = config.COULEUR_ROBOT
                elif pos == self.grille.arrivee:
                    couleur = config.COULEUR_ARRIVEE
                elif self.chemin and pos in self.chemin:
                    couleur = config.COULEUR_CHEMIN
                elif pos in self.grille.obstacles:
                    couleur = config.COULEUR_OBSTACLE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline=config.COULEUR_LIGNES)

    def sur_clic_canvas(self, event):
        """Gère les actions au clic selon le mode choisi (Départ, Arrivée ou Obstacle)."""
        c = event.x // config.TAILLE_CASE
        r = event.y // config.TAILLE_CASE
        position = (r, c)

        # 1. Placement du Départ
        if self.mode_placement == "depart":
            if position != self.grille.arrivee and position not in self.grille.obstacles:
                self.grille.depart = position
                self.mode_placement = "obstacle"  # On revient au mode obstacle par défaut
                self.label_info.config(text="Départ placé avec succès !")
                self.chemin = []
            else:
                self.label_info.config(text="⚠️ Position invalide pour le départ !", fg="red")

        # 2. Placement de l'Arrivée
        elif self.mode_placement == "arrivee":
            if position != self.grille.depart and position not in self.grille.obstacles:
                self.grille.arrivee = position
                self.mode_placement = "obstacle"  # On revient au mode obstacle par défaut
                self.label_info.config(text="Arrivée placée avec succès !")
                self.chemin = []
            else:
                self.label_info.config(text="⚠️ Position invalide pour l'arrivée !", fg="red")

        # 3. Gestion classique des obstacles
        else:
            if position == self.grille.depart or position == self.grille.arrivee:
                return

            if position in self.grille.obstacles:
                self.grille.retirer_obstacle(position)
            else:
                self.grille.ajouter_obstacle(position)
            
            self.chemin = []
            self.label_info.config(text="Cliquez sur la grille pour ajouter des obstacles ou activez le mode dynamique.", fg="black")

        self.dessiner_grille()

    def basculer_dynamique(self):
        """Bascule entre l'activation et l'arrêt des obstacles dynamiques."""
        if not self.simulation_active:
            self.simulation_active = True
            self.btn_dynamique.config(text="Stopper Dynamique", bg="#D32F2F")
            self.label_info.config(text="Obstacles dynamiques activés !")
            self.mettre_a_jour_obstacles_dynamiques()
        else:
            self.simulation_active = False
            self.btn_dynamique.config(text="Activer Dynamique", bg="#FF9800")
            self.label_info.config(text="Obstacles dynamiques stoppés.", fg="black")

    def mettre_a_jour_obstacles_dynamiques(self):
        """Modifie aléatoirement les obstacles et recalcule le BFS en boucle."""
        if not self.simulation_active:
            return

        for r in range(self.grille.lignes):
            for c in range(self.grille.colonnes):
                pos = (r, c)
                if pos == self.grille.depart or pos == self.grille.arrivee:
                    continue
                
                if random.random() < config.PROBA_OBSTACLE:
                    if pos in self.grille.obstacles:
                        self.grille.retirer_obstacle(pos)
                    else:
                        self.grille.ajouter_obstacle(pos)

        nouveau_chemin, self.nb_explores = bfs(self.grille, self.grille.depart, self.grille.arrivee)
        
        if nouveau_chemin is not None:
            self.chemin = nouveau_chemin
            self.label_info.config(text=f"Chemin trouvé (Longueur: {len(self.chemin)}) | Explorés: {self.nb_explores}", fg="black")
            self.dessiner_grille()
            self.root.after(config.INTERVALLE_OBSTACLES_MS, self.mettre_a_jour_obstacles_dynamiques)
        else:
            self.chemin = []
            self.label_info.config(text="⚠️ Aucun chemin trouvé ! Simulation stoppée car bloqué.", fg="red")
            self.dessiner_grille()
            self.simulation_active = False
            self.btn_dynamique.config(text="Activer Dynamique", bg="#FF9800")

    def executer_bfs(self):
        """Lance le BFS manuellement."""
        resultat_chemin, self.nb_explores = bfs(self.grille, self.grille.depart, self.grille.arrivee)
        if resultat_chemin is None:
            self.chemin = []
            self.label_info.config(text=f"⚠️ Aucun chemin trouvé ! Explorés : {self.nb_explores}", fg="red")
        else:
            self.chemin = resultat_chemin
            self.label_info.config(text=f"Chemin trouvé ! Explorés : {self.nb_explores} | Longueur : {len(self.chemin)}", fg="black")
        self.dessiner_grille()

    def reinitialiser_grille(self):
        """Réinitialise la grille et stoppe la simulation."""
        self.simulation_active = False
        self.btn_dynamique.config(text="Activer Dynamique", bg="#FF9800")
        self.grille.obstacles.clear()
        self.chemin = []
        self.mode_placement = "obstacle"
        self.label_info.config(text="Grille réinitialisée.", fg="black")
        self.dessiner_grille()


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotNavApp(root)
    root.mainloop()