#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kev97
#
# Created:     21/06/2022
# Copyright:   (c) kev97 2022
# Licence:     <your licence>
#-----------------------------------------------------------------------------
""" il faut juste a prendre les fonctions normalement, étant donner que les
fenetres sont deja faites """

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import  Image,ImageTk

erreur=0

def afficheImage():
    '''création de la frame et affiche l'image '''
    global img,frameImage

    #importation de l'image
    imgFile=r'C:\Users\kev97\OneDrive\Documents\Mon_pendu\img_pendu\pendu{}.png'.format(erreur)
    photo=Image.open(imgFile)
    photo=photo.resize((250,250),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(photo)


    frameImage=Frame(fenetre)#création de fenetre
    image=Label(frameImage, image=img).pack(side=TOP)#attribution de fenetre a mon image
    frameImage.pack()#affiche fenetre







def creationFrame():
    '''appel la fonction destruction et création de frame '''
    global erreur
    destroyImage()
    erreur+=1
    afficheImage()




def destroyImage():
    '''try except d'oublier la frame '''
    global frameImage
    try : #essaye d'effectuer la commande
        frameImage.forget()#on repack l'image
    except: #sinon il effectue cette commande
        pass

#création fenetre et parametrage

fenetre=Tk()

fenetre.geometry("500x600")
fenetre.title("pendu")
fenetre.minsize(200,100)

frame1=Frame()



boutonA=Button(fenetre, text="A",command=creationFrame)


frame1.pack(side=BOTTOM)
boutonA.pack()
fenetre.mainloop()