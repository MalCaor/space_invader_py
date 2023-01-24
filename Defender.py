from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
from Bullet import Bullet
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
