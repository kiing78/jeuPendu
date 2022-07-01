#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     16/06/2022
# Copyright:   (c) emman 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import easygui
import random
from tkinter import *
from functools import partial
import psycopg2
from PIL import Image, ImageTk

pénalité = 0
messageErreur = ""
word = ""
niveau = ""
lettresProposées = []
secret = ""
win = False
lost = False
theme = ""
dataMot = []
message = ""
databaseUsername= "sebastien"
databaseMdp= "root"
bgColor = "#dedede"
fgColor = "Black"
gagné = False
perdu = False

#------------------------------------------------------------------------------
## ----- Fonctions Liées au jeu -----


def pendu():
    ## Lance le pendu
    creationMainFenetre()
    creationThemeFrame()
    chercheThemeDansDatabase()
    afficheTheme()
    mainFenetre.mainloop()

def victoire():
    ## Retourne un booleen correspondant au statut de victoire
    ## Vérifie si toutes les lettres du mot mystère ont été trouvées et passe le booléen de victoire à True le cas échéant
    global message, clavierFrame, gagné
    if secret.count("_") == 0:
        gagné = True
        for i in range (65, 91):
            lettresProposées.append(chr(i))
        print(lettresProposées)
        updateClavier()
        message = "Bravo vous avez gagné"
        updateMessage()



def defaite():
    ## Retourne un booleen correspondant au statut de défaite
    ## Vérifie si le compteur de pénalité a atteint le max et passe le booléen de défaite à True le cas échéant
    global secret, message, clavierFrame, perdu
    if pénalité == 5:
        perdu = True
        message = "Dommage vous avez perdu"
        updateMessage()
        secret = word
        #secretFrame.destroy()
        #creationSecretFrame()
        updateMotMystere()



def verifLettreValid(event):
    global message, gagné, perdu
    print("Victoire : ", gagné)
    print("Defaite : ", perdu)
    if gagné == False and perdu == False:
        if len(event.char.upper()) != 1:
            message = "Veuillez renseigner 1 et une seule lettre"
            updateMessage()
        elif ord(event.char.upper().upper())<65 or ord(event.char.upper().upper())>90:
            message = "Veuillez renseigner une lettre entre A et Z"
            updateMessage()
        elif event.char.upper() in lettresProposées:
            message = "Vous avez déja proposé cette lettre"
            updateMessage()
        else:
            chercheLettre(event.char.upper())


def chercheLettre(n):
    ## Vérifie si la lettre renseignée est dans le mot, l'ajoute dans le tableau de lettres proposées incrémmente le compteur de pénalité le cas échéant
    global pénalité, lettresProposées, secret, secretFrame, message
    lettre=n
    message = ""
    pénalité = pénalité
    updateMessage()
    # Vérifie les erreurs de proposition de lettre
    letterIsInclude = lettre in word
    lettresProposées.append(lettre)
    updateClavier()
    if (not letterIsInclude):
        pénalité = pénalité + 1
        defaite()
        updateImage()
    else:
        secret = afficheMotSecret()
        victoire()
        secretFrame.destroy()
        creationSecretFrame()


def rejouer():
    ## Relance une partie sur le même theme, même niveau
    global word, pénalité, lettresProposées, message, secret, gagné, perdu
    gagné = False
    perdu = False
    pénalité = 0
    lettresProposées = []
    word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
    secret = afficheMotSecret()
    message = ""
    updateClavier()
    updateMotMystere()
    updateMessage()
    updateImage()


def menu():
    ## Affiche l'écran menu
    global word, pénalité, lettresProposées, theme, niveau, gagné, perdu
    word = ""
    pénalité = 0
    lettresProposées = []
    theme = ""
    niveau = ""
    gagné = False
    perdu = False
    superFrameSecret.destroy()
    superFrameMessage.destroy()
    superFrameClavier.destroy()
    superFrameBoutons.destroy()
    superFrameImage.destroy()
    creationThemeFrame()
    chercheThemeDansDatabase()
    afficheTheme()



#------------------------------------------------------------------------------
## ----- Connexion database -----


def chercheThemeDansDatabase():
    ##Recherche des thèmes dans la database
    global vwtheme
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user=databaseUsername, password=databaseMdp)
    crs = cnx.cursor()
    print("cnx", cnx)
    crs.execute('select * from tb_theme;')
    vwtheme = crs.fetchall()
    crs.close()
    cnx.close()

def chercheNiveauDansDatabase():
    ## Recherche des niveaux dans la database en fonction du thème choisi
    global theme, vwniveau
    t = theme.get()
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user=databaseUsername, password=databaseMdp)
    crs = cnx.cursor()
    crs.execute(f'select * from fx_niveau({t});')
    vwniveau = crs.fetchall()
    crs.close()
    cnx.close()

def chercheMotDansDatabase():
     ## Recherche des mots dans la dataBase en fonction du niveau choisis
    global dataMot
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user=databaseUsername, password=databaseMdp)
    crs = cnx.cursor()
    crs.execute(f'select * from fx_mot2({niveau.get()});')
    dataMot = crs.fetchall()
    crs.close()
    cnx.close()







#------------------------------------------------------------------------------
## ----- Fenetre de jeu -----


#   ------- ECRAN MENU -------

def creationMainFenetre():
    ##Création de la fenêtre principale
    global mainFenetre
    mainFenetre = Tk()
    mainFenetre.title("Pendu")
    mainFenetre.config(bg = bgColor)
    mainFenetre.geometry("400x600")
    mainFenetre.resizable(0,0)


def creationThemeFrame():
    ## Création de la Frame Theme
    global mainFenetre, themeFrame
    themeFrame = Frame (mainFenetre, bg = bgColor)
    themeFrame.pack(pady=20)
    labelTheme = Label(themeFrame, text="THEME", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    labelTheme.pack()


def afficheTheme():
    ## Affichage des thèmes issus de la database dans la frame Thème
    global theme
    theme = StringVar(value=0)
    for t in vwtheme:
        Radiobutton(themeFrame, text=str(list(t)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor,  value= list(t)[0], variable = theme, command=afficheNiveau).pack()


def afficheNiveau():
    ## Recherche des niveaux dans la database - Création de la Frame niveau et affichage des thèmes -----
    global vwniveau, niveauFrame, niveau, boutonPlayFrame, theme
    t=theme.get()
    niveau = StringVar(value=0)
    chercheNiveauDansDatabase()
    destroyNiveauFrame()
    creationNiveauFrame()
    for n in vwniveau:
        Radiobutton(niveauFrame, text=str(list(n)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, value= list(n)[0], variable = niveau, command=creationBoutonPlayFrame).pack()
    #boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")
    #boutonPlayFrame.pack(side=BOTTOM, pady=50)


def destroyNiveauFrame():
    global niveauFrame
    try:
        niveauFrame.destroy()
        destroyBoutonPlay()
    except:
        pass


def creationNiveauFrame():
    ## Création de la Frame niveau
    global niveauFrame
    niveauFrame = Frame (mainFenetre, bg = bgColor)
    niveauFrame.pack()
    labelNiveau = Label(niveauFrame, text="NIVEAU", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    labelNiveau.pack()


def creationBoutonPlayFrame():
    ## Création de la Frame bouton et du bouton PLAY -----
    global boutonPlayFrame, mainFenetre
    destroyBoutonPlay()
    boutonPlayFrame = Frame(mainFenetre, bg = bgColor)
    boutonPlayFrame.pack(side=BOTTOM, pady=50)
    boutonPlay = Button(boutonPlayFrame, text="PLAY", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, command=motMystere)
    boutonPlay.pack()


def destroyBoutonPlay():
    global boutonPlayFrame
    try:
        boutonPlayFrame.destroy()
    except:
        pass





#   ------- ECRAN JEU -------




def motMystere():
    ## Récupère la liste de mots correspondant au niveau sélectionné et selectionne 1 de celui-ci comme mot mystère
    global word, secret, dataMot, secretFrame, clavierFrame
    # Cherche les mots dans la database correspondant au niveau choisi
    chercheMotDansDatabase()

    # Sélection d'1 mot aléatoire
    word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
    # transformation du mot en
    secret = afficheMotSecret()

    # Suppression de la frame bouton -----
    boutonPlayFrame.destroy()
    # Suppression de la frame niveau
    niveauFrame.destroy()
    # Suppression de la frame theme -----
    themeFrame.destroy()

    # Creation de la frame Boutons et des boutons MENU et REJOUER-----
    creationSuperFrameBoutons()
    creationBoutonsFrame()

    # Création de la frame clavier et du clavier
    creationSuperFrameClavier()
    creationClavier()

    # Création de la frame message
    creationSuperFrameMessage()
    creationMessageFrame()

    # Creation de la frame mot secret -----
    creationSuperFrameSecret()
    creationSecretFrame()

    # Creation de la frame Image -----
    creationSuperFrameImage()
    creationFrameImage()



def afficheMotSecret():
    ## Retourne le mot mystère sous forme de "_" ou de lettres en lien avec le tableau de lettres proposées
    global lettresProposées
    secret = ""
    for i in range(len(word)):
        lettreIncluse = False
        for j in range(len(lettresProposées)):
            if lettresProposées[j] == word[i]:
                lettreIncluse = not lettreIncluse
            else:
                lettreIncluse = lettreIncluse
        if lettreIncluse == True or word[i] == " ":
            secret += (word[i]+" ")
            lettreIncluse = not lettreIncluse
        else:
            secret += ("_ ")
    return secret



def creationSuperFrameBoutons():
    global superFrameBoutons
    superFrameBoutons = Frame(mainFenetre, bg = bgColor)
    superFrameBoutons.pack(side=BOTTOM, fill=X)


def creationBoutonsFrame():
    # ----- Etape 14.2 = creation de la frame Boutons qui contiendra les boutons MENU et REJOUER ainsi que ces boutons -----
    global boutonsFrame
    boutonsFrame = Frame(superFrameBoutons, bg = bgColor)
    boutonsFrame.pack(fill=X)

    frameMenu=Frame(boutonsFrame)
    frameRejouer=Frame(boutonsFrame)

    frameMenu.pack(side=LEFT, fill=X, expand=True,)
    frameRejouer.pack(side=RIGHT, fill=X, expand=True,)

    boutonMenu = Button(frameMenu, text="MENU", command=menu, bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    boutonRejouer = Button(frameRejouer, text="REJOUER", command=rejouer, bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    boutonMenu.pack(fill=X)
    boutonRejouer.pack(fill=X)



def creationSuperFrameClavier():
    global superFrameClavier
    superFrameClavier = Frame(mainFenetre, bg = bgColor)
    superFrameClavier.pack(side=BOTTOM, fill=X)




def creationClavier():
    ## Création de la frame et des boutons du clavier
    global clavierFrame, lettresProposées
    clavierFrame = Frame (superFrameClavier, bg = bgColor)
    clavierFrame.bind_all("<Key>", verifLettreValid)
    clavierFrame.pack(side = BOTTOM, pady=20)
    clavierLigne1 = ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"]
    clavierLigne2 = ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"]
    clavierLigne3 = ["W", "X", "C", "V", "B", "N"]


    for lettre in clavierLigne1:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable", bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=0, column=clavierLigne1.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=0, column=clavierLigne1.index(lettre))
    for lettre in clavierLigne2:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable", bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=1, column=clavierLigne2.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=1, column=clavierLigne2.index(lettre))
    for lettre in clavierLigne3:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable", bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=2, column=clavierLigne3.index(lettre)+2)
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=2, column=clavierLigne3.index(lettre)+2)

    clavierFrame.grid_columnconfigure(0, weight=1)
    clavierFrame.grid_columnconfigure(1, weight=1)
    clavierFrame.grid_columnconfigure(2, weight=1)
    clavierFrame.grid_columnconfigure(3, weight=1)
    clavierFrame.grid_columnconfigure(4, weight=1)
    clavierFrame.grid_columnconfigure(5, weight=1)
    clavierFrame.grid_columnconfigure(6, weight=1)
    clavierFrame.grid_columnconfigure(7, weight=1)
    clavierFrame.grid_columnconfigure(8, weight=1)
    clavierFrame.grid_columnconfigure(9, weight=1)



def creationSuperFrameMessage():
    global superFrameMessage
    superFrameMessage = Frame(mainFenetre, bg = bgColor)
    superFrameMessage.pack(side=BOTTOM, fill=X)


def creationMessageFrame():
    global message, messageFrame
    messageFrame = Frame(superFrameMessage, bg = bgColor)
    messageFrame.pack(side=BOTTOM)
    messageLabel = Label(messageFrame, text=message,  bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor)
    messageLabel.pack()


def creationSuperFrameSecret():
    global superFrameSecret
    superFrameSecret = Frame(mainFenetre, bg = bgColor)
    superFrameSecret.pack(side=BOTTOM, fill=X)

def creationSecretFrame():
    # Creation de la frame mot secret -----
    global secretFrame, secret
    secretFrame = Frame(superFrameSecret, bg = bgColor)
    secretLabel = Label(secretFrame, text = secret, bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor)
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)

def creationSuperFrameImage():
    global superFrameImage
    superFrameImage = Frame(mainFenetre, bg = bgColor)
    superFrameImage.pack(side=BOTTOM, fill=BOTH, expand=True)

def creationFrameImage():
    global frameImage
    frameImage = Frame(superFrameImage, bg = bgColor)
    frameImage.pack()
    # Création et plug de l'image dans la Frame Image
    im = Image.open(f"pendu0{pénalité}.png")
    im = im.resize((250, 250))
    photo = ImageTk.PhotoImage(im, master = frameImage)
    labelPhoto = Label(frameImage)
    labelPhoto.img=photo
    labelPhoto.config(image = labelPhoto.img)
    labelPhoto.pack(pady=50)





def updateClavier():
    global clavierFrame, messageFrame, secretFrame
    clavierFrame.destroy()
    creationClavier()
    clavierFrame.pack(side = BOTTOM, pady=20)


def updateMotMystere():
    global secretFrame, secret
    secretFrame.destroy()
    secretFrame = Frame(superFrameSecret, bg = bgColor)
    secretLabel = Label(secretFrame, text = secret, bg = bgColor)
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)


def updateMessage():
    global message, messageFrame
    messageFrame.destroy()
    messageFrame = Frame(superFrameMessage, bg = bgColor)
    messageFrame.pack(side=BOTTOM)
    messageLabel = Label(messageFrame, text=message,  bg = bgColor)
    messageLabel.pack()


def updateImage():
    global frameImage
    frameImage.destroy()
    creationFrameImage()
















#------------------------------------------------------------------------------
## ----- Lancement de la fonction jeu -----

pendu()