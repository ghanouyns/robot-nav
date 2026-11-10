# tests/test_search.py - Tests unitaires pour la recherche BFS

import unittest
import sys
import os

# Force Python à regarder dans le dossier parent pour trouver grid.py et search.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from grid import Grid
from search import bfs

class TestBFS(unittest.TestCase):

    def setUp(self):
        self.grid = Grid(rows=10, cols=10)
        self.grid.start = (0, 0)
        self.grid.goal = (0, 3)

    def test_direct_path(self):
        path, explores = bfs(self.grid, self.grid.start, self.grid.goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (0, 3))
        self.assertEqual(len(path), 4)

if __name__ == '__main__':
    unittest.main()