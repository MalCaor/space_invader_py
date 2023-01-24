from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
from Bullet import Bullet
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