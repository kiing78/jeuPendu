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
    global message
    victoire = False
    if secret.count("_") == 0:
        victoire = True
        messageFrame.destroy()
        message = "Bravo vous avez gagné"
        creationMessageFrame()
    return victoire

def defaite():
    ## Retourne un booleen correspondant au statut de défaite
    ## Vérifie si le compteur de pénalité a atteint le max et passe le booléen de défaite à True le cas échéant
    global secret, message
    defaite = False
    if pénalité == 5:
        defaite = True
        messageFrame.destroy()
        message = "Dommage vous avez perdu"
        creationMessageFrame()
        secret = word
        secretFrame.destroy()
        creationSecretFrame()


    return defaite

def chercheLettre(n):
    ## Vérifie si la lettre renseignée est dans le mot, l'ajoute dans le tableau de lettres proposées incrémmente le compteur de pénalité le cas échéant
    global pénalité, lettresProposées, secret, secretFrame
    lettre=n
    messageErreur = ""
    pénalité = pénalité
    # Vérifie les erreurs de proposition de lettre
    if len(lettre) != 1:
        messageErreur = "Veuillez renseigner 1 et une seule lettre"
        return messageErreur, pénalité
    elif ord(lettre.upper())<65 or ord(lettre.upper())>90:
        messageErreur = "Veuillez renseigner une lettre entre A et Z"
        return messageErreur, pénalité
    elif lettre in lettresProposées:
        messageErreur = "Vous avez déja proposé cette lettre"
        return messageErreur, pénalité
    else:
        letterIsInclude = lettre in word
        lettresProposées.append(lettre)
        updateClavier()
        if (not letterIsInclude):
            pénalité = pénalité + 1
            defaite()
            return messageErreur, pénalité
        else:
            secret = afficheMotSecret()
            victoire()
            secretFrame.destroy()
            creationSecretFrame()


def rejouer():
    print('rejouer')
    ## Relance une partie sur le même theme, même niveau
    global word, pénalité, lettresProposées, message, secret
    pénalité = 0
    lettresProposées = []
    word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
    secret = afficheMotSecret()
    message = ""
    updateClavier()
    updateMotMystere()
    updateMessage()


def menu():
    ## Affiche l'écran menu
    global word, pénalité, lettresProposées, theme, niveau
    word = ""
    pénalité = 0
    lettresProposées = []
    theme = ""
    niveau = ""
    superFrameSecret.destroy()
    superFrameMessage.destroy()
    superFrameClavier.destroy()
    superFrameBoutons.destroy()
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
    print('# ----- Etape 9A = Recherche des mots correspondants au niveau dans la dataBase -----')
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
    mainFenetre.config(bg = "#dedede")
    mainFenetre.geometry("400x600")
    mainFenetre.resizable(0,0)


def creationThemeFrame():
    ## Création de la Frame Theme
    global mainFenetre, themeFrame
    themeFrame = Frame (mainFenetre, bg = "#dedede")
    themeFrame.pack(pady=20)
    labelTheme = Label(themeFrame, text="THEME", bg = "#dedede")
    labelTheme.pack()


def afficheTheme():
    ## Affichage des thèmes issus de la database dans la frame Thème
    global theme
    theme = StringVar(value=0)
    for t in vwtheme:
        Radiobutton(themeFrame, text=str(list(t)[1]), bg = "#dedede", value= list(t)[0], variable = theme, command=afficheNiveau).pack()


def afficheNiveau():
    ## Recherche des niveaux dans la database - Création de la Frame niveau et affichage des thèmes -----
    global vwniveau, niveauFrame, niveau, boutonPlayFrame, theme
    t=theme.get()
    niveau = StringVar(value=0)
    chercheNiveauDansDatabase()
    destroyNiveauFrame()
    creationNiveauFrame()
    for n in vwniveau:
        Radiobutton(niveauFrame, text=str(list(n)[1]), bg = "#dedede", value= list(n)[0], variable = niveau, command=creationBoutonPlayFrame).pack()
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
    niveauFrame = Frame (mainFenetre, bg = "#dedede")
    niveauFrame.pack()
    labelNiveau = Label(niveauFrame, text="NIVEAU", bg = "#dedede")
    labelNiveau.pack()


def creationBoutonPlayFrame():
    ## Création de la Frame bouton et du bouton PLAY -----
    global boutonPlayFrame, mainFenetre
    destroyBoutonPlay()
    boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")
    boutonPlayFrame.pack(side=BOTTOM, pady=50)
    boutonPlay = Button(boutonPlayFrame, text="PLAY", bg = "#dedede", command=motMystere)
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
    superFrameBoutons = Frame(mainFenetre, bg = "#dedede")
    superFrameBoutons.pack(side=BOTTOM, fill=X)


def creationBoutonsFrame():
    # ----- Etape 14.2 = creation de la frame Boutons qui contiendra les boutons MENU et REJOUER ainsi que ces boutons -----
    global boutonsFrame
    boutonsFrame = Frame(superFrameBoutons, bg = "#dedede")
    boutonsFrame.pack(fill=X)

    frameMenu=Frame(boutonsFrame)
    frameRejouer=Frame(boutonsFrame)

    frameMenu.pack(side=LEFT, fill=X, expand=True,)
    frameRejouer.pack(side=RIGHT, fill=X, expand=True,)

    boutonMenu = Button(frameMenu, text="MENU", command=menu)
    boutonRejouer = Button(frameRejouer, text="REJOUER", command=rejouer)
    boutonMenu.pack(fill=X)
    boutonRejouer.pack(fill=X)



def creationSuperFrameClavier():
    global superFrameClavier
    superFrameClavier = Frame(mainFenetre, bg = "#dedede")
    superFrameClavier.pack(side=BOTTOM, fill=X)




def creationClavier():
    ## Création de la frame et des boutons du clavier
    global clavierFrame, lettresProposées
    clavierFrame = Frame (superFrameClavier, bg = "#dedede")
    clavierFrame.pack(side = BOTTOM, pady=20)
    clavierLigne1 = ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"]
    clavierLigne2 = ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"]
    clavierLigne3 = ["W", "X", "C", "V", "B", "N"]


    for lettre in clavierLigne1:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable").grid(row=0, column=clavierLigne1.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre)).grid(row=0, column=clavierLigne1.index(lettre))
    for lettre in clavierLigne2:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable").grid(row=1, column=clavierLigne2.index(lettre))
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre)).grid(row=1, column=clavierLigne2.index(lettre))
    for lettre in clavierLigne3:
        if lettre in lettresProposées:
            Button(clavierFrame, text=lettre, width=20, state="disable").grid(row=2, column=clavierLigne3.index(lettre)+2)
        else:
            Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre)).grid(row=2, column=clavierLigne3.index(lettre)+2)

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
    superFrameMessage = Frame(mainFenetre, bg = "#dedede")
    superFrameMessage.pack(side=BOTTOM, fill=X)


def creationMessageFrame():
    global message, messageFrame
    messageFrame = Frame(superFrameMessage, bg = "#dedede")
    messageFrame.pack(side=BOTTOM)
    messageLabel = Label(messageFrame, text=message,  bg = "#dedede")
    messageLabel.pack()


def creationSuperFrameSecret():
    global superFrameSecret
    superFrameSecret = Frame(mainFenetre, bg = "#dedede")
    superFrameSecret.pack(side=BOTTOM, fill=X)

def creationSecretFrame():
    # Creation de la frame mot secret -----
    global secretFrame, secret
    secretFrame = Frame(superFrameSecret, bg = "#dedede")
    secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)


def updateClavier():
    global clavierFrame, messageFrame, secretFrame
    clavierFrame.destroy()
    creationClavier()
    clavierFrame.pack(side = BOTTOM, pady=20)


def updateMotMystere():
    global secretFrame, secret
    secretFrame.destroy()
    secretFrame = Frame(superFrameSecret, bg = "#dedede")
    secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)


def updateMessage():
    global message, messageFrame
    messageFrame.destroy()
    messageFrame = Frame(superFrameMessage, bg = "#dedede")
    messageFrame.pack(side=BOTTOM)
    messageLabel = Label(messageFrame, text=message,  bg = "#dedede")
    messageLabel.pack()























#------------------------------------------------------------------------------
## ----- Lancement de la fonction jeu -----

pendu()