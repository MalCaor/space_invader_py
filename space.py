# SPACE INVADER !!!

from PIL import ImageTk, Image
import tkinter as tk

class player:
    # Player Class
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.life = 3
        #self.img = tk.PhotoImage(file="img/main_char.png")
        self.img = ImageTk.PhotoImage(Image.open("img/main_char.png"))
        self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        print("player initialized")


class Space:
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
        self.listP = [p]
    
    def start(self):
        for p in self.listP:
            p.imgCanvas = self.canvas.create_image(self.canvas_width // 2, self.canvas_height -10, image=p.imgv2)
            p.x = self.canvas_width // 2
            p.y = self.canvas_height -10
        self.root.mainloop()
        
ex = Space()
ex.install()
ex.start()