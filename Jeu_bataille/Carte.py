import random

class Carte():
    def __init__(self,nom,couleur,valeur,skin="default"):
        self.nom=nom
        self.couleur=couleur
        self.valeur=valeur
        self.skin=skin

def paquet():
    liste=[]
    dico={2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10",11:"Valet",12:"Dame",13:"Roi",14:"as"}
    for couleur in ["carreau", "coeur", "trèfle", "pic"]:
        for i in range(2,15):
            liste.append(Carte(dico[i],couleur,i))
    return liste   

def melange(liste):
    random.shuffle(liste)
    random.shuffle(liste)
    return liste[0:int(len(liste)/2)],liste[int(len(liste)/2)::]
