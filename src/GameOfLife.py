from Logic.Grid import Grid
from Visuals.GUI import GUI

class GameOfLife:
    def __init__(self):
        self.grid = Grid()
        self.gui = GUI(self.grid)