#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kev97
#
# Created:     21/06/2022
# Copyright:   (c) kev97 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------




from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import  Image,ImageTk,ImageSequence
import pygame
import imageio
#fc.run_all()

def afficherRegle():
    """affiche les regles du jeu en pop up """
    phrase= "Règles du jeu L’objectif du pendu est de retrouver un mot “mystère” en découvrant ses lettres.\n Déroulement : \n→ Les lettres du mot “mystère” s’affichent à l’écran sous forme de _ ou autre symbole -Le joueur sélectionne des lettres 1 à 1 \n→Si la lettre est contenue dans le mot, elle apparaît dans le mot mystère à chaque position où elle est présente, elle se bloque pour ne pas être ré-utilisée \n→Si la lettre n’est pas contenue dans le mot On compte une pénalité, elle se bloque pour ne pas être ré-utilisée \n →La partie se termine si je joueur atteint xx pénalités ou s’il découvre le mot mystère"
    messagebox.showinfo("Regle du jeu",phrase)




fenetre= Tk()

fenetre.geometry("500x600")
fenetre.title("selection taille")
fenetre.minsize(200,100)





boutonRegle=Button(fenetre,text="Regle", command=afficherRegle).pack()




fenetre.mainloop()
