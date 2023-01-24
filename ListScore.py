from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
from Score import Score 
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