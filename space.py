# SPACE INVADER !!!

from PIL import ImageTk, Image
import tkinter as tk

class player:
    # Player Class
    def __init__(self, id, canvas, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.mX = 0
        self.mY = 0
        self.life = 3
        self.img = ImageTk.PhotoImage(Image.open("img/main_char.png"))
        self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(x, y, image=self.imgv2)
        print("player initialized")

    def right(self, event):
        print(event.keysym)
        self.mX = 5
        self.mY = 0

    def left(self, event):
        print(event.keysym)
        self.mX = -5
        self.mY = 0

    def movement(self):
        print("move to x:" + str(self.x) + " y:" + str(self.y))
        self.canvas.move(self.sprite, self.mX, self.mY)
        self.canvas.after(100, self.movement)
        # reset to 0 the movement
        self.mX = 0
        self.mY = 0


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
        p = player(i,self.canvas, self.canvas_width // 2, self.canvas_height-10)
        self.listP = [p]
    
    def start(self):
        self.listP[0].movement()
        self.root.bind("<KeyPress-Left>", lambda e: self.listP[0].left(e))
        self.root.bind("<KeyPress-Right>", lambda e: self.listP[0].right(e))
        self.root.mainloop()
        
ex = Space()
ex.install()
ex.start()