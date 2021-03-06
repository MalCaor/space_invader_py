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
        self.type = 'Defender'
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
        # player score
        self.playerScore = 0
        # console message when init finish
        print("player initialized")
        
    def right(self, event):
        # function to move right
        self.mX = 20
        self.mY = 0

    def left(self, event):
        # function to move left
        self.mX = -20
        self.mY = 0

    def shoot(self, event):
        # function to fire/shoot
        if(len(self.fired_bullet) < self.max_fired_bullet):
            bullet = Bullet(self)
            bullet.install_in_Defender()
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

    def update(self, allFleet):
        # function update
        for b in self.fired_bullet:
            b.update_Defender(allFleet)

    def takeHit(self):
        self.life = self.life - 1
        #retire des points si touché
        self.playerScore = self.playerScore - 5

        if(self.playerScore < 0):
            # pas de score négatif
            self.playerScore = 0

        if(self.life <= 0):
            self.death()

    def death(self):
        # Explosion animation !!!!
        print("perdu")



class Bullet:
    def __init__(self,shooter):
        self.radius = 6

        if(shooter.type == 'Defender'):
            self.color = "blue"
            self.speed = 8
        elif(shooter.type == 'Alien'):
            self.color = "red"
            self.speed = 6

        self.y =0
        self.x=0
        
        self.shooter = shooter
        self.canvas = shooter.canvas

    def install_in_Defender(self):
        self.bullet_id = self.canvas.create_oval(self.shooter.x-self.radius, self.shooter.y-50-self.radius, self.shooter.x+self.radius, self.shooter.y-50+self.radius, fill=self.color) 
        self.y = self.shooter.y-50-self.radius
        self.x = self.shooter.x

    def update_Defender(self, allFleet):
        self.move_in_Defender()
        if(self.y < 0):
            self.delete_Defender()
            return 0
        x1, y1, x2, y2 = self.canvas.bbox(self.bullet_id)
        listA = self.canvas.find_overlapping(x1, y1, x2, y2)
        for f in allFleet:
            for l in f.fleet:
                for a in l:
                    if(a.sprite in listA):
                        self.delete_Defender()
                        a.delete(l)
                        self.shooter.playerScore = self.shooter.playerScore + 10
                        return 0
    
    def move_in_Defender(self):
        self.canvas.move(self.bullet_id, 0, -(self.speed))
        self.y = self.y-self.speed

    def delete_Defender(self):
        self.shooter.fired_bullet.remove(self)
        self.canvas.delete(self.bullet_id)
    
    def install_in_Alien(self):
        self.bullet_id = self.canvas.create_oval(self.shooter.x-self.radius, self.shooter.y+25-self.radius, self.shooter.x+self.radius, self.shooter.y+25+self.radius, fill=self.color) 
        self.y = self.shooter.y+50-self.radius
        self.x = self.shooter.x

    def update_Alien(self, fleet, hauteur, listP):
        self.move_in_Alien()
        if(self.y > hauteur+25):
            self.delete_Alien(fleet)
            return 0
        x1, y1, x2, y2 = self.canvas.bbox(self.bullet_id)
        listOverlap = self.canvas.find_overlapping(x1, y1, x2, y2)
        for p in listP:
            if(p.sprite in listOverlap):
                self.delete_Alien(fleet)
                p.takeHit()
    
    def move_in_Alien(self):
        self.canvas.move(self.bullet_id, 0, +(self.speed))
        self.y = self.y+self.speed

    def delete_Alien(self, fleet):
        fleet.fired_bullet.remove(self)
        self.shooter.fired_bullet = self.shooter.fired_bullet-1
        self.canvas.delete(self.bullet_id)



class Alien:
    def __init__(self, x, y, canvas):
        # type
        self.type = 'Alien'
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
            bullet = Bullet(self)
            bullet.install_in_Alien()
            self.fired_bullet = self.fired_bullet+1
            fleet.fired_bullet.append(bullet)

    def delete(self, line):
        self.canvas.delete(self.sprite)
        line.remove(self)

    

class Fleet:
    # groupe d alien
    def __init__(self, canvas):
        self.fleet = []
        self.orientation = 0
        self.canvas = canvas
        # set fleet reinforcement = if True, the fleet already receive reinforcement
        self.reinforcement = False
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
            
    def moveOrComeBack(self, spaceInv, largeur, hauteur, listP):
        i = 0
        # largeur est la limite de l'ecran
        for line in self.fleet:
            # pour chaque ligne
            for a in line:
                # update chaque alien
                a.update(self, largeur, hauteur)
                i = i + 1
        # move bullet
        if(i <= 0):
            self.delete(spaceInv)

        for b in self.fired_bullet:
            b.update_Alien(self, hauteur, listP)

    def delete(self, parent):
        parent.allFleet.remove(self)
        for b in self.fired_bullet:
            b.delete_Alien(self)
                

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
            #créer un score
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
        
        
        # config canvas
        self.canvas_width = 600
        self.canvas_height = 400
        self.square_width = 50
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height = self.canvas_height)
        self.canvas.pack()
        self.allFleet = []
        


    def install(self):
        # create background
        self.canvas.create_rectangle(0,0, self.canvas_width, self.canvas_height, fill='black')
        # create player 
        p = Defender(1,self.canvas, self.canvas_width // 2, self.canvas_height-10)
        self.listP = [p]
        # create fleet
        fleet = Fleet(self.canvas)
        self.allFleet.append(fleet)
        self.canvas_width = int(self.canvas.cget("width"))
        self.canvas_height = int(self.canvas.cget("height"))
        x, y = self.canvas_width//10, self.canvas_height//10 
        self.allFleet[0].install_in(x, y)
        self.scoreText = None
    


    def start_animation(self):
        # execute self.animation dans 10ms
        self.canvas.after(10, self.animation)



    def animation(self):
        
        for uneFleet in self.allFleet:
            uneFleet.moveOrComeBack(self, int(self.canvas.cget("width")), int(self.canvas.cget("height")), self.listP)

            # count number alien
            nbAlien=0
            for line in uneFleet.fleet:
                for alien in line:
                    nbAlien = nbAlien+1
            # envoie du renfort
            if(nbAlien<=3 and uneFleet.reinforcement==False):
                newFleet = Fleet(self.canvas)
                self.allFleet.append(newFleet)
                self.allFleet[len(self.allFleet)-1].install_in(self.canvas_width//10, self.canvas_height//10)
                uneFleet.reinforcement = True
            # quand une flotte est detruite
            if(nbAlien == 0):
                for player in self.listP:
                    player.life = player.life + 1
                    print('+1 Vie')
                for bullet in uneFleet.fired_bullet:
                    bullet.delete_Alien(uneFleet)

        #Affichage du Score et des Vies
        for p in self.listP:
            p.update(self.allFleet)
            highestScore = 0
            pseudoHighestScore = ''
            for score in self.lesScores.listScore:
                if(highestScore < score.score):
                    highestScore = score.score
                    pseudoHighestScore = score.player
            if (self.pseudo == None or self.pseudo == ""):
                self.pseudo = "player"
            if(self.scoreText != None):
                self.canvas.delete(self.scoreText)
            else:
                self.canvas.create_text(self.canvas_width/2,10,fill="white",font="Arial 10",text= "Highest Score")
                self.canvas.create_text(self.canvas_width/2,25,fill="white",font="Arial 10",text= pseudoHighestScore+" : "+str(highestScore))
            self.scoreText = self.canvas.create_text(100,10,fill="white",text= self.pseudo+" : "+str(p.playerScore)+"   Vies = "+str(p.life))
                
        #Continue ou Fin du jeu
        for p in self.listP:
            if(not self.allFleet or p.life <= 0):
                self.end(p)
            else:
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
    


    def end(self,player):
        print('Game Over')
        if(self.pseudo == None):
            self.pseudo = 'player'+str(player.id)
        print(str(self.pseudo)+' : '+str(player.playerScore))
        
        # Saving score
        leScore = Score(self.pseudo, player.playerScore)
        self.lesScores.listScore.append(leScore)
        # TODO : temp fix to test writing score
        self.lesScores.toFile("score.json")
        




ex = SpaceInvader()
ex.start()