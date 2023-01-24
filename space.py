# SPACE INVADER !!!

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
from Defender import Defender
from Fleet import Fleet
from Score import Score 
from ListScore import ListScore

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
        # fuction on loop
        self.listP[0].movement()
        # key binding
        self.root.bind("<KeyPress-Left>", lambda e: self.listP[0].left(e))
        self.root.bind("<KeyPress-Right>", lambda e: self.listP[0].right(e))
        self.root.bind("<KeyPress-space>", lambda e: self.listP[0].shoot(e))
    


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
        # etc...
        self.start_animation()
        self.root.mainloop()

    def reset(self):
        # unbind key
        self.root.unbind("<KeyPress-r>")
        #delet les fleet
        for f in self.allFleet :
            f.delete(self)
        self.install()
        self.animation()

    def end(self,player):
        # display Game Over
        print('Game Over')
        self.canvas.create_text(self.canvas_width/2,self.canvas_height/2,fill="white",font="Arial 20",text= "Game Over")
        self.canvas.create_text(self.canvas_width/2,self.canvas_height/2+25,fill="white",font="Arial 12",text= "Score : " + str(self.listP[0].playerScore))
        # print score
        if(self.pseudo == None):
            self.pseudo = 'player'+str(player.id)
        print(str(self.pseudo)+' : '+str(player.playerScore))
        # Saving score
        leScore = Score(self.pseudo, player.playerScore)
        self.lesScores.listScore.append(leScore)
        # TODO : temp fix to test writing score
        self.lesScores.toFile("score.json")
        # retry
        print('bind')
        self.root.bind("<KeyPress-r>", lambda e: self.reset())
        self.canvas.create_text(self.canvas_width/2,self.canvas_height/2+50,fill="white",font="Arial 10",text= "Press R to retry")

ex = SpaceInvader()
ex.start()