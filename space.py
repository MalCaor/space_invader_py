# SPACE INVADER !!!

from PIL import ImageTk, Image
import tkinter as tk

class player:
    # Player Class
    def __init__(self, id, canvas, x, y):
        # player id
        self.id = id
        # player pos
        self.x = x
        self.y = y
        # player movement
        self.mX = 0
        self.mY = 0
        # player lives
        self.life = 3
        # player sprite
        self.img = ImageTk.PhotoImage(Image.open("img/main_char.png"))
        self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        self.canvas = canvas
        self.sprite = self.canvas.create_image(x, y, image=self.imgv2)
        # console message when init finish
        print("player initialized")

    def right(self, event):
        # function to move right
        print(event.keysym)
        self.mX = 5
        self.mY = 0

    def left(self, event):
        # function to move left
        print(event.keysym)
        self.mX = -5
        self.mY = 0

    def movement(self):
        # fuction called to move
        print("move to x:" + str(self.x) + " y:" + str(self.y))
        self.canvas.move(self.sprite, self.mX, self.mY)
        self.canvas.after(100, self.movement)
        # reset to 0 the movement
        self.mX = 0
        self.mY = 0


class Space:
    def __init__(self):
        # init canvas
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
        # fuction on loop
        self.listP[0].movement()
        # key binding
        self.root.bind("<KeyPress-Left>", lambda e: self.listP[0].left(e))
        self.root.bind("<KeyPress-Right>", lambda e: self.listP[0].right(e))
        # etc...
        self.root.mainloop()
        
ex = Space()
ex.install()
ex.start()