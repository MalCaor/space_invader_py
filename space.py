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
        
    def right(self, event):
        # function to move right
        self.mX = 10
        self.mY = 0

    def left(self, event):
        # function to move left
        self.mX = -10
        self.mY = 0

    def shoot(self, event):
        # function to fire/shoot
        if(len(self.fired_bullet) < self.max_fired_bullet):
            bullet = Bullet(self)
            bullet.install_in()
            self.fired_bullet.append(bullet)

    def movement(self):
        # fuction called to move
        self.canvas.move(self.sprite, self.mX, self.mY)
        self.canvas.after(100, self.movement)
        self.x = self.x + self.mX
        self.y = self.y + self.mY
        # reset to 0 the movement
        self.mX = 0
        self.mY = 0

    def update(self, fleet):
        # function update
        for b in self.fired_bullet:
            b.update(fleet)



class Bullet:
    def __init__(self,shooter):
        self.radius = 6
        self.color = "red"
        self.speed = 8
        self.y =0
        self.x=0
        
        self.shooter = shooter
        self.canvas = shooter.canvas

    def install_in(self):
        self.bullet_id = self.canvas.create_rectangle(self.shooter.x-self.radius, self.shooter.y-50-self.radius, self.shooter.x+self.radius, self.shooter.y-50+self.radius, fill=self.color) 
        self.y = self.shooter.y-50-self.radius
        self.x = self.shooter.x

    def update(self, fleet):
        self.move_in()
        if(self.y < 0):
            self.delete()
            return 0
        x1, y1, x2, y2 = self.canvas.bbox(self.bullet_id)
        listA = self.canvas.find_overlapping(x1, y1, x2, y2)
        for l in fleet.fleet:
            for a in l:
                if(a.sprite in listA):
                    self.delete()
                    a.delete(l)
                    return 0
    
    def move_in(self):
        self.canvas.move(self.bullet_id, 0, -(self.speed))
        self.y = self.y-self.speed

    def delete(self):
        self.shooter.fired_bullet.remove(self)
        self.canvas.delete(self.bullet_id)
    




class Alien:
    def __init__(self, x, y, canvas):
        # position de l'alien
        self.x = x
        self.y = y
        # canvas
        self.canvas = canvas
        # gap est le mouvement de l'alien
        self.gap = 3
        # sprite de l'alien (imgv2 est une image plus grande de l'alien)
        self.img = ImageTk.PhotoImage(Image.open("img/enemy_char.png"))
        self.imgv2 = self.img._PhotoImage__photo.zoom(2)
        self.sprite = self.canvas.create_image(x, y, image=self.imgv2)
        # direction est vers ou ce deplace l'alien, 0 il va a droite, 1 a gauche
        self.direction = 0
        # shoot
        self.max_fired_bullet = 1
        self.fired_bullet = 0

    
    def setGap(self, gap):
        # set le gap (si on a besoin d'augmenter/reduire la vitesse)
        self.gap = gap

    def moveOrComeBack(self):
        # alien movement
        if(self.direction == 0): 
            # vers la droite           
            self.canvas.move(self.sprite, self.gap, 0)
            self.x = self.x+self.gap
        if(self.direction == 1):
            # vers la gauche
            self.canvas.move(self.sprite, -(self.gap), 0)
            self.x = self.x-self.gap

    def goDown(self):
        # va en bas
        self.canvas.move(self.sprite, 0, 15)
        self.y = self.y+15

    def update(self, fleet, largeur, hauteur):
        # fonction update a chaque tic
        if (self.direction == 0):
            # si il va a droite
            if (self.x + self.gap > largeur):
                # si il touche le mur
                self.direction = 1
                self.goDown()
                self.moveOrComeBack()
            else:
                # deplacement normal
                self.moveOrComeBack()
        elif (self.direction == 1):
            # si il va a gauche
            if (self.x - self.gap < 0):
                # si il touche le mur
                self.direction = 0
                self.goDown()
                self.moveOrComeBack()
            else:
                # deplacement normal
                self.moveOrComeBack()
        # update bullet
        self.shoot(fleet)
        

    def shoot(self, fleet):
        # function to fire/shoot
        if(self.fired_bullet < self.max_fired_bullet):
            bullet = BulletAlien(self)
            bullet.install_in()
            self.fired_bullet = self.fired_bullet+1
            fleet.fired_bullet.append(bullet)

    def delete(self, line):
        self.canvas.delete(self.sprite)
        line.remove(self)

class BulletAlien:
    def __init__(self,shooter):
        self.radius = 6
        self.color = "red"
        self.speed = 8
        self.y =0
        self.x=0
        # shooter
        self.shooter = shooter
        self.canvas = shooter.canvas

    def install_in(self):
        self.bullet_id = self.canvas.create_rectangle(self.shooter.x-self.radius, self.shooter.y+25-self.radius, self.shooter.x+self.radius, self.shooter.y+25+self.radius, fill=self.color) 
        self.y = self.shooter.y+50-self.radius
        self.x = self.shooter.x

    def update(self, fleet, hauteur):
        self.move_in()
        if(self.y > hauteur):
            self.delete(fleet)
            return 0
        x1, y1, x2, y2 = self.canvas.bbox(self.bullet_id)
        listOverlap = self.canvas.find_overlapping(x1, y1, x2, y2)
    
    def move_in(self):
        self.canvas.move(self.bullet_id, 0, +(self.speed))
        self.y = self.y+self.speed

    def delete(self, fleet):
        fleet.fired_bullet.remove(self)
        self.shooter.fired_bullet = self.shooter.fired_bullet-1
        self.canvas.delete(self.bullet_id)

class Fleet:
    # groupe d alien
    def __init__(self, canvas):
        self.fleet = []
        self.orientation = 0
        self.canvas = canvas
        # bullet
        self.fired_bullet = []
    
    def install_in(self, x, y):
        for i in range(3):  #change value to change fleet size (nb line)
            line = []
            for j in range(5):  #change value to change fleet size (nb alien in line)
                x = x + 40
                line.append(Alien(x,y,self.canvas))
            self.fleet.append(line)
            x = x - (j+1)*40
            y = y + 40
            
    def moveOrComeBack(self, largeur, hauteur):
        # largeur est la limite de l'ecran
        for line in self.fleet:
            # pour chaque ligne
            for a in line:
                # update chaque alien
                a.update(self, largeur, hauteur)
        # move bullet
        for b in self.fired_bullet:
            b.update(self, hauteur)

class Score:
    def __init__(self, player, score):
        self.player = player
        self.score = score

    # acces fichier
    def toFile(self, fileName):
        f = open(fileName,"w")
        l=self
        json.dump(l.__dict__,f)
        f.close()

    @classmethod
    def fromFile(cls, fileName):
        f = open(fileName,"r")
        d = json.load(f)
        newScore=Score(d["player"],d["score"])
        f.close()
        return newScore

    def __str__(self):
        return str(self.player) + " : " + str(self.score)

class ListScore:
    def __init__(self):
        self.listScore = []

     # acces fichier
    def toFile(self, fileName):
        f = open(fileName,"w")
        tmp = []
        for s in self.listScore:
        #créer un dictionnaire
            d = {}
            d["player"] = s.player
            d["score"] = s.score
            tmp.append(d)
        json.dump(tmp,f)
        f.close()

    @classmethod
    def fromFile(cls,fileName):
        if not os.path.exists(fileName):
            f = open(fileName,"w")
            f.write("[]")
        f = open(fileName,"r")
        #chargement
        tmp = json.load(f)
        liste = []
        for d in tmp:
            #créer un scre
            l=Score(d["player"],d["score"])
            #l'ajouter dans la liste
            liste.append(l)
        vretour=ListScore()
        vretour.listScore=liste
        f.close()
        return vretour

    def __str__(self):
        vretour = "list Score : \n"
        for s in self.listScore:
            vretour = vretour+str(s)+"\n"
        vretour = vretour.rstrip(vretour[-1])
        return vretour



class SpaceInvader:
    def __init__(self):
        # init canvas
        self.root = tk.Tk()
        # pseudo 
        self.pseudo = simpledialog.askstring(title="Pseudo",prompt="What is your Pseudo?:")
        self.lesScores = ListScore.fromFile("score.json")
        leScore = Score(self.pseudo, 0)
        self.lesScores.listScore.append(leScore)
        # TODO : temp fix to test writing score
        self.lesScores.toFile("score.json")
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
        p = Defender(1,self.canvas, self.canvas_width // 2, self.canvas_height-10)
        self.listP = [p]
        # create fleet
        self.fleet = Fleet(self.canvas)
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        x, y = canvas_width//10, canvas_height//10 
        self.fleet.install_in(x, y)
    
    def start_animation(self):
        # execute self.animation dans 10ms
        self.canvas.after(10, self.animation)

    def animation(self):
        self.fleet.moveOrComeBack(int(self.canvas.cget("width")), int(self.canvas.cget("height")))     # need to change the "8"
        for p in self.listP:
            p.update(self.fleet)
        # execute a nouveau self.animation dans 300ms
        self.canvas.after(25, self.animation)
    
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




ex = SpaceInvader()
ex.start()