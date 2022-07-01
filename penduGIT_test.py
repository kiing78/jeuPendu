import easygui
import random
from tkinter import *
from functools import partial
import psycopg2
import imageio
from PIL import Image,ImageTk,ImageSequence

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

## ----- Création de la fênetre de jeu -----

## ----- Connexion à la database pour récupérer les thèmes et niveaux disponibles -----

## ----- Définition des fonctions qui lancent le jeu -----
def pendu():
    ## Lance le pendu
     ## Définition des variables
      # Variables Globales qui seront appelées et modifiées dans des fonctions

      # Variables locales -dans la fonction pendu()- qui ne seront pas modifiées dans les fonctions


    creationMainFenetre()
    creationThemeFrame()
    chercheThemeDansDatabase()
    afficheTheme()
    #creationNiveauFrame()
    #chercheNiveauDansDatabase()
    #Création et affichage de la frame thème
    mainFenetre.mainloop()


## ----- Fonctions Liées au jeu -----

def victoire():
    ## Vérifie si toutes les lettres du mot mystère ont été trouvées et passe le booléen de victoire à True le cas échéant
    global secret, message, labelImgPendun, img5
    victoire = False
    if secret.count("_") == 0:
        victoire = True
        print("Bravo vous avez gagné")
        messageFrame.destroy()
        message = "Bravo vous avez gagné"
        creationMessageFrame()
        secret = word
        secretFrame.destroy()
        creationSecretFrame()
        secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
        secretLabel.pack()
        secretFrame.pack(side = BOTTOM, pady=20)
        ## msgbox ("Bravo, vous avez gagné", title = "pendu")
    return victoire

def defaite():
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
        secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
        secretLabel.pack()
        secretFrame.pack(side = BOTTOM, pady=20)
        print("Dommage, vous avez perdu")
    return defaite

def chercheLettre(n):
    ## Vérifie si la lettre renseignée est dans le mot, l'ajoute dans le tableau de lettres proposées incrémmente le compteur de pénalité le cas échéant
    # ----- Etape 17 = Vérification de la lettre sélectionnée -----
    print('# ----- Etape 17 = Vérification de la lettre sélectionnée -----')
    print('welcome in chercheLettre : ', n)
    global pénalité, lettresProposées, secret, secretFrame
    lettre=n
    messageErreur = ""
    pénalité = pénalité
    print("pénalité : ", pénalité)
    print("messageErreur : ", messageErreur)
    if len(lettre) != 1:
        print("erreur 1")
        messageErreur = "Veuillez renseigner 1 et une seule lettre"
        return messageErreur, pénalité
    elif ord(lettre.upper())<65 or ord(lettre.upper())>90:
        print("erreur 2")
        messageErreur = "Veuillez renseigner une lettre entre A et Z"
        return messageErreur, pénalité
    elif lettre in lettresProposées:
        print("erreur 3")
        messageErreur = "Vous avez déja proposé cette lettre"
        return messageErreur, pénalité
    else:
        print("pas d'erreur")
        letterIsInclude = lettre in word
        lettresProposées.append(lettre)
        if (not letterIsInclude):
            print("La lettre n'est pas incluse")
            pénalité = pénalité + 1
            addImgPendu()
            defaite()
            return messageErreur, pénalité
        else:
            print("La lettre est incluse")
            secret = afficheMotSecret()
            if secret.count("_") == 0:
                pénalité = 6
                addImgPendu()
            victoire()
            print('secretFrame : ', secretFrame)
            try:
                secretFrame.destroy()
            except:
                pass
            creationSecretFrame()
            secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
            secretLabel.pack()
            secretFrame.pack(side = BOTTOM, pady=20)

def rejouer():
    global word, pénalité, lettresProposées, message, labelImgPendu, imPenduframe
    pénalité = 0
    lettresProposées = []
    word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
    secret = afficheMotSecret()
    try:
        secretFrame.destroy()
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, bg = '#dedede')
        labelImgPendu.pack()
    except:
        pass
    messageFrame.destroy()
    message = ""
    creationMessageFrame()
    creationSecretFrame()
    secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)

def menu():
    ## Réinitialise toutes les variables relatives au jeu, supprime les frames relatives au jeu et "recharge" les frames relatives au menu
    global word, pénalité, lettresProposées, theme, niveau, imPenduframe
    word = ""
    pénalité = 0
    lettresProposées = []
    theme = ""
    niveau = ""
    imPenduframe.destroy()
    secretFrame.destroy()
    messageFrame.destroy()
    clavierFrame.destroy()
    boutonsFrame.destroy()
    creationThemeFrame()
    chercheThemeDansDatabase()
    afficheTheme()

## ----- Connexion database -----


def chercheThemeDansDatabase():
    # ----- Etape 3 = Recherche des thèmes dans la database -----
    print('# ----- Etape 3 = Recherche des thèmes dans la database -----')
    global vwtheme
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='sebastien', password='root')
    crs = cnx.cursor()
    ## Execution des requêtes et enregistrement du resultat dans des variables
    crs.execute('select * from tb_theme;')
    vwtheme = crs.fetchall()
    ## Fermeture de la connexion
    crs.close()
    cnx.close()

def chercheNiveauDansDatabase():
    # ----- Etape 5A = Recherche des niveaux dans la database -----
    print('# ----- Etape 5A = Recherche des niveaux dans la database -----')
    global theme, vwniveau
    t = theme.get()
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='sebastien', password='root')
    crs = cnx.cursor()
    crs.execute(f'select * from fx_niveau({t});')
    vwniveau = crs.fetchall()
    crs.close()
    cnx.close()

def chercheMotDansDatabase():
     # ----- Etape 9A = Recherche des mots correspondants au niveau dans la dataBase -----
    print('# ----- Etape 9A = Recherche des mots correspondants au niveau dans la dataBase -----')
    global dataMot
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='sebastien', password='root')
    crs = cnx.cursor()
    crs.execute(f'select * from fx_mot2({niveau.get()});')
    dataMot = crs.fetchall()
    crs.close()
    cnx.close()



## ----- Fenetre de jeu -----

def creationClavier():
    ## Création de la frame et des boutons du clavier
    global clavierFrame, current_lettre
    # ----- Etape 15A = Création de la frame clavier -----
    print('# ----- Etape 15A = Création de la frame clavier -----')
    clavierFrame = Frame (mainFenetre, bg = "#dedede")
    # ----- Etape 15B = Création du clavier -----
    print('# ----- Etape 15B = Création du clavier -----')
    clavierLigne1 = ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"]
    clavierLigne2 = ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"]
    clavierLigne3 = ["W", "X", "C", "V", "B", "N"]
    current_lettre=()
    for lettre in clavierLigne1:
        Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre)).grid(row=0, column=clavierLigne1.index(lettre))
    for lettre in clavierLigne2:
        Button(clavierFrame, text=lettre, width=20, command=partial(chercheLettre, lettre)).grid(row=1, column=clavierLigne2.index(lettre))
    for lettre in clavierLigne3:
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

def creationSecretFrame():
    # ----- Etape 14 = creation de la frame mot secret -----
    print('# ----- Etape 14 = creation de la frame mot secret -----')
    global secretFrame
    secretFrame = Frame(mainFenetre, bg = "#dedede")

def creationFrameImgPendu():
    global imPenduframe, labelImgPendu
    imPenduframe = Frame(mainFenetre, width=400, height=300)
    imPenduframe.pack(side=TOP)
    labelImgPendu = Label(imPenduframe, bg = '#dedede')
    labelImgPendu.pack()

def addImgPendu():
    global imPenduframe, labelImgPendu, img5, imgL
    if pénalité == 0:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, bg = '#dedede')
        labelImgPendu.pack()
    elif pénalité == 1:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, image = img1)
        labelImgPendu.pack()
    elif pénalité == 2:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, image = img2)
        labelImgPendu.pack()
    elif pénalité == 3:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, image = img3)
        labelImgPendu.pack()
    elif pénalité == 4:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe, image = img4)
        labelImgPendu.pack()
    elif pénalité == 5:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe)
        labelImgPendu.pack()
        for imgL in ImageSequence.Iterator(imgL):
            imgL=ImageTk.PhotoImage(imgL)
            for speed in range(1000):
                labelImgPendu.config(image=imgL)
            imPenduframe.update()
    elif pénalité == 6:
        labelImgPendu.destroy()
        labelImgPendu = Label(imPenduframe)
        labelImgPendu.pack()
        for img5 in ImageSequence.Iterator(img5):
            img5=ImageTk.PhotoImage(img5)
            for speed in range(1000):
                labelImgPendu.config(image=img5)
            imPenduframe.update()

def creationBoutonsFrame():
    # ----- Etape 14.2 = creation de la frame Boutons qui contiendra les boutons MENU et REJOUER ainsi que ces boutons -----
    print('# ----- Etape 14.2 = creation de la frame mot secret -----')
    global boutonsFrame
    boutonsFrame = Frame(mainFenetre, bg = "#dedede")
    boutonsFrame.pack(side=BOTTOM, fill=X)

    frameMenu=Frame(boutonsFrame)
    frameRejouer=Frame(boutonsFrame)

    frameMenu.pack(side=LEFT, fill=X, expand=True,)
    frameRejouer.pack(side=RIGHT, fill=X, expand=True,)

    boutonMenu = Button(frameMenu, text="MENU", command=menu)
    boutonRejouer = Button(frameRejouer, text="REJOUER", command=rejouer)
    boutonMenu.pack(fill=X)
    boutonRejouer.pack(fill=X)



def motMystere():
    ## Récupère la liste de mots correspondant au niveau sélectionné et selectionne 1 de celui-ci comme mot mystère
    # ----- Etape 9 = Recherche des mots correspondants au niveau dans la dataBase -----
    print('# ----- Etape 9 = Recherche des mots correspondants au niveau dans la dataBase -----')
    global word, secret, dataMot, secretFrame, clavierFrame
    chercheMotDansDatabase()
    # ----- Etape 9B = Sélection d'1 mot aléatoire -----
    print("# ----- Etape 9B = Sélection d'1 mot aléatoire -----")
    word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
    # ----- Etape 10 = transformation du mot en _ _ _ -----
    print('# ----- Etape 10 = transformation du mot en _ _ _ -----')
    secret = afficheMotSecret()
    # ----- Etape 11 = Suppression de la frame bouton -----
    print('# ----- Etape 11 = Suppression de la frame bouton -----')
    boutonPlayFrame.destroy()
    # ----- Etape 12 = Suppression de la frame niveau -----
    print('# ----- Etape 12 = Suppression de la frame niveau -----')
    niveauFrame.destroy()
    # ----- Etape 13 = Suppression de la frame theme -----
    print('# ----- Etape 13 = Suppression de la frame theme -----')
    themeFrame.destroy()
    # ----- Etape 14.1 = creation de la frame Boutons -----
    print('# ----- Etape 14.1 = creation de la frame Boutons -----')
    creationBoutonsFrame()
    # ----- Etape 14.1 = creation de la frame Boutons -----
    print('# ----- Etape 14.2 = creation de la frame Image du Pendu -----')
    creationFrameImgPendu()
    # ----- Etape 14 = creation de la frame mot secret -----
    print('# ----- Etape 14 = creation de la frame mot secret -----')
    creationSecretFrame()
    # ----- Etape 15 = Création de la frame clavier et du clavier -----
    print('# ----- Etape 15 = Création de la frame clavier et du clavier -----')
    creationClavier()
    # ----- Etape 15C = Affichage de la frame Clavier -----
    print('# ----- Etape 15C = Affichage de la frame Clavier -----')
    clavierFrame.pack(side = BOTTOM, pady=20)
    print('# ----- Création et affichage de la frame Message')
    creationMessageFrame()

    # ----- Etape 16 = Création et affichage  de la frame image de pendu -----
##    print('# ----- Etape 16 = Création et affichage  de la frame image de pendu -----')
##    imPenduframe = Frame(secretFrame, width=400, height=300)
##    imPenduframe.pack(side=TOP)
    # ----- Etape 17 = Création et affichage  de la frame mot secret -----
    print('# ----- Etape 17 = Création et affichage  de la frame mot secret -----')
    secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)

def creationMessageFrame():
    global message, messageFrame
    messageFrame = Frame(mainFenetre, bg = "#dedede")
    messageFrame.pack(side=BOTTOM)
    messageLabel = Label(messageFrame, text=message,  bg = "#dedede")
    messageLabel.pack()



def creationBoutonPlayFrame():
    # ----- Etape 8 = Création de la Frame bouton et du bouton PLAY -----
    print('# ----- Etape 8 = Création de la Frame bouton et du bouton PLAY -----')
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

def destroyNiveauFrame():
    global niveauFrame
    try:
        niveauFrame.destroy()
        destroyBoutonPlay()
    except:
        pass

def creationNiveauFrame():
    # ----- Etape 7A = Création de la Frame niveau -----
    print('# ----- Etape 7A = Création de la Frame niveau -----')
    global niveauFrame
    niveauFrame = Frame (mainFenetre, bg = "#dedede")
    niveauFrame.pack()
    labelNiveau = Label(niveauFrame, text="NIVEAU", bg = "#dedede")
    labelNiveau.pack()

def afficheNiveau():
    # ----- Etape 5 = Recherche des niveaux dans la database - Création de la Frame niveau et affichage des thèmes -----
    print('# ----- Etape 5 = Recherche des niveaux dans la database - Création de la Frame niveau et affichage des thèmes -----')
    global vwniveau, niveauFrame, niveau, boutonPlayFrame, theme
    t=theme.get()
    niveau = StringVar(value=0)
    chercheNiveauDansDatabase()
    # ----- Etape 6 = Suppression du Bouton PLAY et du niveau existant en cas de changement de theme -----
    print('# ----- Etape 6 = Suppression du Bouton PLAY et du niveau existant en cas de changement de theme -----')
    destroyNiveauFrame()
    # ----- Etape 7 = Création de la Frame niveau et affichage des thèmes -----
    print('# ----- Etape 7 = Création de la Frame niveau et affichage des thèmes -----')
    creationNiveauFrame()
    # ----- Etape 7B = Affichage des themes -----
    print('# ----- Etape 7B = Affichage des themes -----')
    for n in vwniveau:
        Radiobutton(niveauFrame, text=str(list(n)[1]), bg = "#dedede", value= list(n)[0], variable = niveau, command=creationBoutonPlayFrame).pack()
    #boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")
    #boutonPlayFrame.pack(side=BOTTOM, pady=50)


def creationMainFenetre():
    # ----- Etape 1 = Création de la fenêtre principale -----
    print('# ----- Etape 1 = Création de la fenêtre principale -----')
    global mainFenetre
    mainFenetre = Tk()
    mainFenetre.title("Pendu")
    mainFenetre.config(bg = "#dedede")
    mainFenetre.geometry("400x600")
    mainFenetre.resizable(0,0)
    global img1, img2, img3, img4, img5, imgL
    img1 = PhotoImage(file="n1.png")
    img2 = PhotoImage(file="n2.png")
    img3 = PhotoImage(file="n3.png")
    img4 = PhotoImage(file="n4.png")
    img5 = Image.open("fireworks.gif")
    imgL = Image.open("fireworks.gif")

def creationThemeFrame():
    # ----- Etape 2 = Création de la Frame Theme -----
    print('# ----- Etape 2 = Création de la Frame Theme -----')
    global mainFenetre, themeFrame
    themeFrame = Frame (mainFenetre, bg = "#dedede")
    themeFrame.pack(pady=20)
    labelTheme = Label(themeFrame, text="THEME", bg = "#dedede")
    labelTheme.pack()

def afficheTheme():
    # ----- Etape 4 = Affichage des thèmes issus de la database dans la frame Thème -----
    print('# ----- Etape 4 = Affichage des thèmes issus de la database dans la frame Thème -----')
    global theme
    theme = StringVar(value=0)
    for t in vwtheme:
        print('t : ', t)
        Radiobutton(themeFrame, text=str(list(t)[1]), bg = "#dedede", value= list(t)[0], variable = theme, command=afficheNiveau).pack()



def afficheMotSecret():
    ## Affiche le mot mystère sous forme de "_" ou de lettres en lien avec le tableau de lettres proposées
    print('# ----- Etape 10A = transformation du mot en _ _ _ -----')
    global lettresProposées
    global lettreIncluse
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

## ----- Lancement de la fonction jeu -----
pendu()