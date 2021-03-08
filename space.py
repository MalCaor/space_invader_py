# SPACE INVADER !!!

import tkinter as tk

class player:
    # Player Class
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.life = 3
        print("player initialized")


class Example:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas_width = 600
        self.canvas_height = 400
        self.square_width = 50
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height = self.canvas_height)
        self.canvas.pack()

    def install(self):
        w, h  = self.canvas_width // 2, self.canvas_height // 2
        sw = self.square_width
        # create player 
        i = 1
        p = player(i)
    
    def start(self):
        self.root.mainloop()
        
ex = Example()
ex.install()
ex.start()