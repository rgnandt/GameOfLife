from .Logic.Grid import Grid
from .Visuals.GUI import GUI

class GameOfLife:
    def __init__(self, grid_height: int = 30, grid_width: int = 30):
        self.grid = Grid(height=grid_height, width=grid_width)
        self.gui = GUI(self.grid)