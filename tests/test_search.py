
import unittest

from grid import Grille
from search import bfs


class TestBFS(unittest.TestCase):

    # ==========================================
    # Test 1 : Vérifier qu'un chemin existe
    # ==========================================

    def test_chemin_existe(self):

        grille = Grille(5, 5)

        depart = (0, 0)
        arrivee = (4, 4)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertIsNotNone(chemin)

        self.assertEqual(chemin[0], depart)
        self.assertEqual(chemin[-1], arrivee)

        self.assertGreater(explores, 0)

    # ==========================================
    # Test 2 : Vérifier le chemin le plus court
    # ==========================================

    def test_chemin_plus_court(self):

        grille = Grille(3, 3)

        depart = (0, 0)
        arrivee = (2, 2)

        chemin, explores = bfs(grille, depart, arrivee)

        # 4 déplacements sont nécessaires
        self.assertEqual(len(chemin) - 1, 4)

    # ==========================================
    # Test 3 : Vérifier les obstacles
    # ==========================================

    def test_avec_obstacles(self):

        grille = Grille(5, 5)

        grille.ajouter_obstacle((0, 1))
        grille.ajouter_obstacle((1, 1))
        grille.ajouter_obstacle((2, 1))

        depart = (0, 0)
        arrivee = (0, 2)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertIsNotNone(chemin)

        # Vérifier que le chemin ne traverse aucun obstacle
        for case in chemin:
            self.assertNotIn(case, grille.obstacles)

    # ==========================================
    # Test 4 : Aucun chemin possible
    # ==========================================

    def test_aucun_chemin(self):

        grille = Grille(3, 3)

        # Bloquer toute une colonne
        grille.ajouter_obstacle((0, 1))
        grille.ajouter_obstacle((1, 1))
        grille.ajouter_obstacle((2, 1))

        depart = (1, 0)
        arrivee = (1, 2)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertIsNone(chemin)

    # ==========================================
    # Test 5 : Départ bloqué
    # ==========================================

    def test_depart_bloque(self):

        grille = Grille(5, 5)

        depart = (0, 0)
        arrivee = (4, 4)

        grille.ajouter_obstacle(depart)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertIsNone(chemin)
        self.assertEqual(explores, 0)

    # ==========================================
    # Test 6 : Arrivée bloquée
    # ==========================================

    def test_arrivee_bloquee(self):

        grille = Grille(5, 5)

        depart = (0, 0)
        arrivee = (4, 4)

        grille.ajouter_obstacle(arrivee)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertIsNone(chemin)
        self.assertEqual(explores, 0)

    # ==========================================
    # Test 7 : Départ = Arrivée
    # ==========================================

    def test_depart_egal_arrivee(self):

        grille = Grille(5, 5)

        depart = (2, 2)
        arrivee = (2, 2)

        chemin, explores = bfs(grille, depart, arrivee)

        self.assertEqual(chemin, [depart])
        self.assertEqual(explores, 1)

    # ==========================================
    # Test 8 : Vérifier les déplacements
    # ==========================================

    def test_deplacements_valides(self):

        grille = Grille(5, 5)

        depart = (0, 0)
        arrivee = (4, 4)

        chemin, explores = bfs(grille, depart, arrivee)

        for i in range(len(chemin) - 1):

            ligne1, colonne1 = chemin[i]
            ligne2, colonne2 = chemin[i + 1]

            distance = abs(ligne1 - ligne2) + abs(colonne1 - colonne2)

            self.assertEqual(distance, 1)
    
    # ==========================================
    # Test 9 : Génération des obstacles
    # ==========================================

    def test_generation_obstacles(self):

        grille = Grille(20, 20)

        grille.generer_obstacles_aleatoires()

        self.assertGreater(len(grille.obstacles), 0)

    # ==========================================
    # Test 10 : Départ et arrivée libres
    # ==========================================

    def test_depart_arrivee_libres_apres_generation(self):

        grille = Grille(20, 20)

        grille.generer_obstacles_aleatoires()

        self.assertNotIn(grille.depart, grille.obstacles)
        self.assertNotIn(grille.arrivee, grille.obstacles)

    # ==========================================
    # Test 11 : Obstacles dans les limites
    # ==========================================

    def test_obstacles_dans_grille(self):

        grille = Grille(20, 20)

        grille.generer_obstacles_aleatoires()

        for case in grille.obstacles:
            self.assertTrue(grille.dans_grille(case))


# ==========================================
# Exécution des tests
# ==========================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
