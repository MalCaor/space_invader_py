from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
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
