# ui.py - Interface graphique du projet robot-nav avec Tkinter

import tkinter as tk
from config import ROWS, COLS, CELL_SIZE, COLOR_EMPTY, COLOR_OBSTACLE, COLOR_START, COLOR_GOAL, COLOR_PATH, COLOR_VISITED
from grid import Grid
from search import bfs

class RobotNavApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigation Intelligente de Robot - Niveaux 1 & 2 (BFS)")

        # Initialisation de la grille
        self.grid = Grid(ROWS, COLS)

        # Variables d'état
        self.path = []
        self.explored_count = 0

        # Création des éléments de l'interface
        self.create_widgets()
        self.draw_grid()

    def create_widgets(self):
        """Crée les boutons de contrôle et le Canvas pour la grille."""
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        btn_run = tk.Button(control_frame, text="Lancer BFS", command=self.run_bfs, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_run.pack(side=tk.LEFT, padx=5)

        btn_clear = tk.Button(control_frame, text="Réinitialiser", command=self.reset_grid, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
        btn_clear.pack(side=tk.LEFT, padx=5)

        self.label_info = tk.Label(control_frame, text="Cliquez sur la grille pour ajouter/retirer des obstacles", font=("Arial", 10))
        self.label_info.pack(side=tk.RIGHT, padx=5)

        # Calcul de la taille du Canvas en pixels
        canvas_width = self.grid.cols * CELL_SIZE
        canvas_height = self.grid.rows * CELL_SIZE
        
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Association du clic de la souris pour dessiner les obstacles
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_grid(self):
        """Dessine toutes les cellules de la grille avec leurs couleurs respectives."""
        self.canvas.delete("all")

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                pos = (r, c)
                color = COLOR_EMPTY

                if pos == self.grid.start:
                    color = COLOR_START
                elif pos == self.grid.goal:
                    color = COLOR_GOAL
                elif pos in self.path:
                    color = COLOR_PATH
                elif pos in self.grid.obstacles:
                    color = COLOR_OBSTACLE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#d3d3d3")

    def on_canvas_click(self, event):
        """Gère le clic de la souris sur le Canvas pour basculer l'état d'une case (obstacle ou non)."""
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE
        position = (r, c)

        self.grid.toggle_obstacle(position)
        self.path = []  # Réinitialise le chemin si les obstacles changent
        self.draw_grid()

    def run_bfs(self):
        """Exécute l'algorithme BFS et affiche le résultat sur l'interface."""
        self.path, self.explored_count = bfs(self.grid, self.grid.start, self.grid.goal)
        
        if self.path is None:
            self.label_info.config(text="Aucun chemin trouvé !")
        else:
            self.label_info.config(text=f"Chemin trouvé ! Cases explorées : {self.explored_count} | Longueur : {len(self.path)}")

        self.draw_grid()

    def reset_grid(self):
        """Remet à zéro les obstacles et le chemin affiché."""
        self.grid.obstacles.clear()
        self.path = []
        self.label_info.config(text="Grille réinitialisée.")
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotNavApp(root)
    root.mainloop()