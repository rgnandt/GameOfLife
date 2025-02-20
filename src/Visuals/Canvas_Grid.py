import tkinter as tk
from tkinter import ttk
from src.Logic.Grid import Grid

class CanvasGrid():
    def __init__(self, parent: ttk.Frame, _grid: Grid):
        self.parent = parent
        self.grid = _grid
        self.square_side = 20
        self.width = self.grid.width * self.square_side
        self.height = self.grid.height * self.square_side
        self.alive_color = 'black'
        self.dead_color = 'white'
        self.user_interaction = True

        self.canvas = tk.Canvas(self.parent, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag_left_click)
        self.canvas.bind("<ButtonRelease-1>", self.reset_buffer)
        self.canvas.bind("<B3-Motion>", self.drag_right_click)
        self.canvas.bind("<ButtonRelease-3>", self.reset_buffer)
        self.click_buffer = set()

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.draw_square(x, y)

    def draw_square(self, x, y):
        _x = x*self.square_side
        _y = y*self.square_side
        color = self.alive_color if self.grid.is_alive(x, y) else self.dead_color
        self.canvas.create_rectangle(_x, _y, _x+self.square_side, _y+self.square_side, fill=color, outline=color)

    def screen_to_grid(self, x, y):
        return x // self.square_side, y // self.square_side

    def click(self, event):
        if self.user_interaction:
            x, y = self.screen_to_grid(event.x, event.y)
            self.grid.toggle_field(x, y)
            self.draw()
            # add to buffer to prevent setting tile to alive after it was just toggled to dead
            self.click_buffer.add((x, y))

    def drag_left_click(self, event):
        if self.user_interaction:
            x, y = self.screen_to_grid(event.x, event.y)
            if (x, y) not in self.click_buffer:
                self.grid.set_field(x, y, 1)
                self.draw()
                self.click_buffer.add((x, y))

    def drag_right_click(self, event):
        if self.user_interaction:
            x, y = self.screen_to_grid(event.x, event.y)
            if (x, y) not in self.click_buffer:
                self.grid.set_field(x, y, 0)
                self.draw()
                self.click_buffer.add((x, y))

    def reset_buffer(self, event=None):
        self.click_buffer = set()
