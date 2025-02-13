import tkinter as tk
from tkinter import ttk
from src.Logic import Grid
from .Canvas_Grid import CanvasGrid

class GUI(tk.Tk):
    def __init__(self, grid: Grid):
        super().__init__()
        self.resizable(False, False)
        self.grid = grid
        self.title("Game of Life")

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(row=0, column=0)
        self.grid_visualizer = CanvasGrid(self.grid_frame, grid)

        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=1, column=0)
        self.set_up_buttons()

        self.running = False
        self.mainloop()

    def set_up_buttons(self):
        self.buttons = dict()
        self.button_functions = {"Start": self.run, "Stop": self.stop, "Step": self.step_forward,
                                "Step back": self.step_backward, "Clear": self.clear}

        for name, function in self.button_functions.items():
            self.buttons[name] = ttk.Button(self.control_frame, text=name, command=function)

        for i, button in enumerate(self.buttons.values()):
            button.grid(row=0, column=i)

    def update_screen(self):
        self.grid_visualizer.draw()

    def step_forward(self):
        self.grid.step()
        self.update_screen()

    def step_backward(self):
        self.grid.step_back()
        self.update_screen()

    def tick(self):
        if self.running:
            self.grid.step()
            self.update_screen()
            self.after(500, self.tick)

    def run(self):
        self.running = True
        self.grid_visualizer.user_interaction = False
        self.after(1, self.tick)

        for name, button in self.buttons.items():
            if name != "Stop":
                button.config(state=tk.DISABLED)

    def stop(self):
        self.running = False
        self.grid_visualizer.user_interaction = True

        for button in self.buttons.values():
            button.config(state=tk.NORMAL)

    def clear(self):
        self.grid.clear_grid()
        self.update_screen()