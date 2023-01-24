from PIL import ImageTk, Image
import tkinter as tk
from tkinter import simpledialog
import json
import os
import random
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