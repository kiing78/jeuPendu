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
databaseUsername= "emmanuel"
databaseMdp= "Tournevis@00"
bgColor = "#dedede"
fgColor = "Black"
gagné = False
perdu = False

#------------------------------------------------------------------------------
## ----- Fonctions Liées au jeu -----


def pendu():
    ## Lance le pendu
    creationMainFenetre()
    creationSuperFrameImage("top")
    creationFrameImageAccueil()
    creationBoutonReglesFrame()
    creationBoutonStartFrame()
    mainFenetre.mainloop()

def victoire():
    ## Retourne un booleen correspondant au statut de victoire
    ## Vérifie si toutes les lettres du mot mystère ont été trouvées et passe le booléen de victoire à True le cas échéant
    global message, clavierFrame, gagné
    if secret.count("_") == 0:
        gagné = True
        for i in range (65, 91):
            lettresProposées.append(chr(i))
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


#   ------- ECRAN ACCUEIL -------

def creationMainFenetre():
    ##Création de la fenêtre principale
    global mainFenetre
    mainFenetre = Tk()
    mainFenetre.title("Pendu")
    mainFenetre.config(bg = bgColor)
    mainFenetre.geometry("400x600")
    mainFenetre.resizable(0,0)


def creationBoutonReglesFrame():
    ## Création de la Frame Bouton Règles
    global mainFenetre, boutonReglesFrame
    boutonReglesFrame = Frame (mainFenetre, bg = bgColor)
    boutonReglesFrame.pack(pady=20)
    boutonRegles = Button(boutonReglesFrame, text="REGLES", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    boutonRegles.pack()


def creationBoutonStartFrame():
    ## Création de la Frame Bouton Start
    global mainFenetre, boutonStartFrame
    boutonStartFrame = Frame (mainFenetre, bg = bgColor)
    boutonStartFrame.pack(pady=20)
    boutonRegles = Button(boutonStartFrame, text="START", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, command = goToMenu)
    boutonRegles.pack()


def creationFrameImageAccueil():
    global frameImage
    frameImage = Frame(superFrameImage, bg = bgColor)
    frameImage.pack()
    # Création et plug de l'image dans la Frame Image
    im = Image.open(f"lependu.png")
    im = im.resize((250, 250))
    photo = ImageTk.PhotoImage(im, master = frameImage)
    labelPhoto = Label(frameImage)
    labelPhoto.img=photo
    labelPhoto.config(image = labelPhoto.img)
    labelPhoto.pack(pady=50)

def goToMenu():
    boutonReglesFrame.destroy()
    boutonStartFrame.destroy()
    superFrameImage.destroy()
    creationBoutonRetourAccueilFrame()
    creationThemeFrame()
    chercheThemeDansDatabase()
    afficheTheme()



#   ------- ECRAN MENU -------

def creationThemeFrame():
    ## Création de la Frame Theme
    global mainFenetre, themeFrame
    themeFrame = Frame (mainFenetre, bg = bgColor)
    themeFrame.pack(pady=20)
    labelTheme = Label(themeFrame, text="THEME", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor)
    labelTheme.grid(row=0, column=0, columnspan = 2)


def afficheTheme():
    ## Affichage des thèmes issus de la database dans la frame Thème
    global theme
    theme = StringVar(value=0)
    col = 0
    row = 1
    for t in vwtheme:
        if vwtheme.index(t)%2 !=0:
            Radiobutton(themeFrame, text=str(list(t)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor,  value= list(t)[0], variable = theme, command=afficheNiveau).grid(row=row, column=col)
            row +=1
            col =0
        else:
            Radiobutton(themeFrame, text=str(list(t)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor,  value= list(t)[0], variable = theme, command=afficheNiveau).grid(row=row, column=col)
            col += 1
def afficheNiveau():
    ## Recherche des niveaux dans la database - Création de la Frame niveau et affichage des thèmes -----
    global vwniveau, niveauFrame, niveau, boutonPlayFrame, theme
    #t=theme.get()
    niveau = StringVar(value=0)
    chercheNiveauDansDatabase()
    destroyNiveauFrame()
    creationNiveauFrame()
    col = 0
    row = 1
    for n in vwniveau:
        if vwniveau.index(n)%2 !=0:
            Radiobutton(niveauFrame, text=str(list(n)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, value= list(n)[0], variable = niveau, command=creationBoutonPlayFrame).grid(row=row, column=col)
            row +=1
            col =0
        else:
            Radiobutton(niveauFrame, text=str(list(n)[1]), bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, value= list(n)[0], variable = niveau, command=creationBoutonPlayFrame).grid(row=row, column=col)
            col += 1
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
    labelNiveau.grid(row=0, column=0, columnspan=2)


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


def goToAccueil():
    # Suppression de la frame bouton -----
    try:
        boutonPlayFrame.destroy()
    except:
        pass
    # Suppression de la frame niveau
    try:
        niveauFrame.destroy()
    except:
        pass
    # Suppression de la frame theme -----
    try:
        themeFrame.destroy()
    except:
        pass
    try:
        boutonRetourAccueilFrame.destroy()
    except:
        pass
    creationSuperFrameImage("top")
    creationFrameImage()
    creationBoutonReglesFrame()
    creationBoutonStartFrame()


def affiche():
    print("clic")

def creationBoutonRetourAccueilFrame():
    ## Création de la Frame Bouton Retour Accueil
    global mainFenetre, boutonRetourAccueilFrame, boutonRetourAccueil, im, fleche
    boutonRetourAccueilFrame = Frame (mainFenetre, bg = bgColor)
    boutonRetourAccueilFrame.pack( fill=BOTH, side=TOP, pady=10, padx=10)

    im = Image.open(r"D:\Manu\FORMATIONS\PYTHON\PENDU\penduGIT\jeuPendu\return.png")
    #im.show()
    im = im.resize((30,30), Image.ANTIALIAS)
    fleche = ImageTk.PhotoImage(im)

    #boutonRetourAccueil = Button(boutonRetourAccueilFrame, image=fleche,  bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, compound=CENTER)
    boutonRetourAccueil = Button(boutonRetourAccueilFrame, image=fleche, bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, command = goToAccueil, borderwidth=0)
    boutonRetourAccueil.pack(side=LEFT,)





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
    # Suppression de la frame retour Accueil Bouton
    boutonRetourAccueilFrame.destroy()

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
    creationSuperFrameImage('bottom')
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
        if lettreIncluse == True:
            secret += (word[i]+" ")
            lettreIncluse = not lettreIncluse
        elif word[i] == " ":
            secret += (word[i]+"  ")
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
            if lettre in word:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#81b29a", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=0, column=clavierLigne1.index(lettre))
            else:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#ffa69e", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=0, column=clavierLigne1.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=lambda e=lettre:chercheLettre(e), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=0, column=clavierLigne1.index(lettre))
    for lettre in clavierLigne2:
        if lettre in lettresProposées:
            if lettre in word:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#81b29a", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=1, column=clavierLigne2.index(lettre))
            else:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#ffa69e", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=1, column=clavierLigne2.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=lambda e=lettre:chercheLettre(e), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=1, column=clavierLigne2.index(lettre))
    for lettre in clavierLigne3:
        if lettre in lettresProposées:
            if lettre in word:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#81b29a", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=2, column=2+clavierLigne3.index(lettre))
            else:
                Button(clavierFrame, text=lettre, width=20, state="disable", bg = "#ffa69e", fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=2, column=2+clavierLigne3.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=lambda e=lettre:chercheLettre(e), bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor).grid(row=2, column=2+clavierLigne3.index(lettre))

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
    # Creation de la frame mot secret
    global secretFrame, secret
    secretFrame = Frame(superFrameSecret, bg = bgColor)
    secretLabel = Label(secretFrame, text = secret, bg = bgColor, fg= fgColor, activebackground = bgColor, activeforeground = fgColor)
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)

def creationSuperFrameImage(side):
    global superFrameImage
    superFrameImage = Frame(mainFenetre, bg = bgColor)
    superFrameImage.pack(side=side, fill=BOTH, expand=True)

def creationFrameImage():
    global frameImage
    frameImage = Frame(superFrameImage, bg = bgColor)
    frameImage.pack()
    # Création et plug de l'image dans la Frame Image
    im = Image.open(f"image{pénalité}.png")
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




'''

##Création de la fenêtre principale
global mainFenetre
mainFenetre = Tk()
mainFenetre.title("Pendu")
mainFenetre.config(bg = bgColor)
mainFenetre.geometry("400x600")
mainFenetre.resizable(0,0)





boutonRetourAccueilFrame = Frame (mainFenetre, bg = 'red')
boutonRetourAccueilFrame.pack()

im = Image.open(r"D:\Manu\FORMATIONS\PYTHON\PENDU\penduGIT\jeuPendu\return.png")
#im.show()
im = im.resize((30,30), Image.ANTIALIAS)
fleche = ImageTk.PhotoImage(im)

boutonRetourAccueil = Button(boutonRetourAccueilFrame, image=fleche, text="a", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, command = affiche, compound=CENTER)
#boutonRetourAccueil = Button(boutonRetourAccueilFrame, text="ACCUEIL", bg = bgColor, fg = fgColor, activebackground = bgColor, activeforeground = fgColor, command = goToAccueil)
boutonRetourAccueil.pack()




mainFenetre.mainloop()


'''





#------------------------------------------------------------------------------
## ----- Lancement de la fonction jeu -----

pendu()