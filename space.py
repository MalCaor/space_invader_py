# SPACE INVADER !!!

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os

class Defender:
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
        # player bullets
        self.max_fired_bullet = 8
        self.fired_bullet = []
        # console message when init finish
        print("player initialized")
        
    def shoot(self, event):
        # function to fire/shoot
        print(event.keysym)
        self.fired_bullet.append(Bullet(self))
        current_bullet = len(self.fired_bullet)-1
        self.fired_bullet[current_bullet].install_in()

    def right(self, event):
        # function to move right
        print(event.keysym)
        self.mX = 10
        self.mY = 0

    def left(self, event):
        # function to move left
        print(event.keysym)
        self.mX = -10
        self.mY = 0

    def movement(self):
        # fuction called to move
        #print("move to x:" + str(self.x) + " y:" + str(self.y))
        self.canvas.move(self.sprite, self.mX, self.mY)
        self.canvas.after(100, self.movement)
        # reset to 0 the movement
        self.mX = 0
        self.mY = 0



class Bullet:
    def __init__(self,shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.bullet_id = None
        self.shooter = shooter

    def install_in(self):
        self.bullet_id = self.shooter.canvas.create_oval(self.shooter.mX,self.shooter.mY+10,self.shooter.mX+self.radius,self.shooter.mY+10)

    
    def move_in(self,canvas):
        return 0 #temp
    




class Alien:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.gap = 20
        #self.alien_id = None
        self.img = ImageTk.PhotoImage(Image.open("img/enemy_char.png"))
        self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        self.sprite = self.canvas.create_image(x, y, image=self.imgv2)
        # alien sprite
        #self.img = ImageTk.PhotoImage(Image.open("img/alien.png"))
        #self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        #self.sprite = self.canvas.create_image(x, y, image=self.imgv2)
        

    def install_in(self):
        w = 20
        # self.alien_id = self.canvas.create_rectangle(self.x-w/2, self.y-w/2, self.x+w/2, self.y+w/2, fill="red")

    def setGap(self, gap):
        self.gap = gap

    def moveOrComeBack(self):
        # alien movement
        self.canvas.move(self.sprite, self.gap, 0)

    def goDown(self):
        self.canvas.move(self.sprite, 0, 30)



class Fleet:
    def __init__(self, canvas):
        self.fleet = []
        self.est = 0
        self.west = 0
        self.orientation = 0
        self.canvas = canvas

        self.est = 0
        self.west = 0
        self.orientation = 0
    
    def install_in(self):
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        x, y = canvas_width//10, canvas_height//10        # need to change values, pas ouf pas ouf
        
        self.west = x

        for i in range(3):  #change value to change fleet size (nb line)
            line = []
            for j in range(5):  #change value to change fleet size (nb alien in line)
                x = x + 40
                line.append(Alien(x,y,self.canvas))
                line[j].install_in()
                self.est = x+20
            self.fleet.append(line)
            x = x - (j+1)*40
            y = y + 40
            
    def moveOrComeBack(self, largeur):
        #largeur = int(self.canvas.cget("width"))
        if(self.west-40 < 0):
            #print("west")
            self.orientation = 0
            for line in self.fleet:
                for a in line:
                    a.goDown()
                    a.setGap(20)
        if(self.est+40 > largeur):
            #print("est")
            self.orientation = 1
            for line in self.fleet:
                for a in line:
                    a.goDown()
                    a.setGap(-20)
        for line in self.fleet:
            for a in line:
                a.moveOrComeBack()
                if(self.orientation == 0):
                    self.est = self.est+20
                    self.west = self.west+20
                else:
                    self.est = self.est-20
                    self.west = self.west-20

class Score:
    def __init__(self, nom, score):
        self.nom = nom
        self.score = score

    # acces fichier
    def toFile(self, nomF):
        f = open(nomF,"w")
        l=self
        json.dump(l.__dict__,f)
        f.close()

    @classmethod
    def fromFile(cls, fich):
        f = open(fich,"r")
        d = json.load(f)
        lnew=Score(d["nom"],d["score"])
        f.close()
        return lnew

    def __str__(self):
        return str(self.nom) + " : " + str(self.score)

class listScore:
    def __init__(self):
        self.listScore = []

     # acces fichier
    def toFile(self, nomF):
        f = open(nomF,"w")
        tmp = []
        for s in self.listScore:
        #créer un dictionnaire
            d = {}
            d["nom"] = s.nom
            d["score"] = s.score
            tmp.append(d)
        json.dump(tmp,f)
        f.close()

    @classmethod
    def fromFile(cls,fich):
        if not os.path.exists(fich):
            f = open(fich,"w")
            f.write("[]")
        f = open(fich,"r")
        #chargement
        tmp = json.load(f)
        liste = []
        for d in tmp:
            #créer un scre
            l=Score(d["nom"],d["score"])
            #l'ajouter dans la liste
            liste.append(l)
        lib=listScore()
        lib.listScore=liste
        f.close()
        return lib

    def __str__(self):
        retour = "list Score : \n"
        for s in self.listScore:
            retour = retour+str(s)+"\n"
        retour = retour.rstrip(retour[-1])
        return retour



class Space:
    def __init__(self):
        # init canvas
        self.root = tk.Tk()
        # pseudo 
        self.pseudo = simpledialog.askstring(title="Pseudo",prompt="What's your Pseudo?:")
        self.score = listScore.fromFile("score.json")
        s = Score(self.pseudo, 0)
        self.score.listScore.append(s)
        # TODO : temp fix to test writing score
        self.score.toFile("score.json")
        # config canvas
        self.canvas_width = 600
        self.canvas_height = 400
        self.square_width = 50
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height = self.canvas_height)
        self.canvas.pack()
        self.fleet = None
        


    def install(self):
        # create background
        self.canvas.create_rectangle(0,0, self.canvas_width, self.canvas_height, fill='black')
        # create player 
        i = 1
        p = Defender(i,self.canvas, self.canvas_width // 2, self.canvas_height-10)
        self.listP = [p]
        # create fleet
        self.fleet = Fleet(self.canvas)
        self.fleet.install_in()
    
    def start_animation(self):
        # execute self.animation dans 10ms
        self.canvas.after(10, self.animation)

    def animation(self):
        self.fleet.moveOrComeBack(int(self.canvas.cget("width"))*8)     # need to change the "8"
        # execute a nouveau self.animation dans 300ms
        self.canvas.after(300, self.animation)
    
    def start(self):
        self.install()
        # fuction on loop
        self.listP[0].movement()
        # key binding
        self.root.bind("<KeyPress-Left>", lambda e: self.listP[0].left(e))
        self.root.bind("<KeyPress-Right>", lambda e: self.listP[0].right(e))
        self.root.bind("<KeyPress-space>", lambda e: self.listP[0].shoot(e))
        # etc...
        self.start_animation()
        self.root.mainloop()




ex = Space()
ex.start()