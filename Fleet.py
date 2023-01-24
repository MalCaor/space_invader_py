from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
from Alien import Alien
class Fleet:
    # groupe d alien
    def __init__(self, canvas):
        self.fleet = []
        self.orientation = 0
        self.canvas = canvas
        # set fleet reinforcement = if True, that fleet already receive reinforcement
        self.reinforcement = False
        # bullet
        self.fired_bullet = []

        self.minLineRandom = 2
        self.maxLineRandom = 4
        self.minAlienRandom = 4
        self.maxAlienRandom = 6


    
    def install_in(self, x, y):
        
        for i in range(random.randrange(self.minLineRandom, self.maxLineRandom)):  #change value to change fleet size (nb line)
            line = []
            for j in range(random.randrange(self.minAlienRandom, self.maxAlienRandom)):  #change value to change fleet size (nb alien in line)
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