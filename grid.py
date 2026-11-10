# grid.py - Modèle de la grille pour le projet robot-nav

class Grid:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.start = (1, 1)
        self.goal = (18, 18)
        self.obstacles = set()

    def in_bounds(self, position):
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_free(self, position):
        return self.in_bounds(position) and position not in self.obstacles

    def neighbors(self, position):
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in directions:
            neighbor = (row + dr, col + dc)
            if self.is_free(neighbor):
                result.append(neighbor)
        return result

    def toggle_obstacle(self, position):
        if not self.in_bounds(position):
            return
        if position == self.start or position == self.goal:
            return
        if position in self.obstacles:
            self.obstacles.remove(position)
        else:
            self.obstacles.add(position)