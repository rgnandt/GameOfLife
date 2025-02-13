import random

class Grid:
    def __init__(self, height: int=30, width: int=30):
        self.width = width
        self.height = height
        self.alive, self.dead = 1, 0
        self.grid = [[]]
        self.random_grid()
        self.neighbor_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.set_neighbor_grid()
        self.grid_history = []

    def alternating_grid(self):
        self.grid = [[(j+i)%2 for i in range(self.width)] for j in range(self.height)]

    def random_grid(self):
        self.grid = [random.choices([self.dead, self.alive], [4, 1], k=self.width)
                     for _ in range(self.height)]

    def set_neighbor_grid(self):
        for y in range(self.height):
            for x in range(self.width):
                self.neighbor_grid[y][x] = self.get_alive_neighbors(x, y)

    def set_field(self, height: int, width: int, value: int):
        assert value in [self.alive, self.dead], "ILLEGAL GRID VALUE"
        self.grid[height][width] = value
        self.set_neighbor_grid()

    def get_field(self, height: int, width: int):
        return self.grid[height][width]

    def is_alive(self, height: int, width: int):
        return self.grid[height][width] == self.alive

    def toggle_field(self, height: int, width: int):
        self.set_field(height, width, self.dead if self.is_alive(height, width) else self.alive)

    def get_alive_neighbors(self, x: int, y: int):
        neighbors = 0
        for dx in range(-1, 2):
            if not 0 <= x+dx < self.width:
                continue
            for dy in range(-1, 2):
                if (dx==0) and (dy==0):
                    continue
                elif not 0 <= y+dy < self.height:
                    continue
                elif self.grid[y+dy][x+dx] == self.alive:
                    neighbors += 1
        return neighbors

    def clear_grid(self):
        self.grid_history.append(self.grid)
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.set_neighbor_grid()

    def step(self):
        _grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = self.neighbor_grid[y][x]
                state = self.dead
                if self.grid[y][x] == self.alive:
                    if 2 <= alive_neighbors <= 3:
                        state = self.alive
                else:
                    if alive_neighbors == 3:
                        state = self.alive
                _grid[y][x] = state
        self.grid_history.append(self.grid)
        self.grid = _grid
        self.set_neighbor_grid()

    def step_back(self):
        if self.grid_history:
            self.grid = self.grid_history.pop(-1)
            self.set_neighbor_grid()