#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     02/06/2022
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

    '''
    def boutonPlay():
        ## Affiche un bouton PLAY fois le thème choisi pour déterminer le mot choisi
        global boutonPlayFrame
        boutonPlayFrame.destroy()
        boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")
        boutonPlayFrame.pack(side = BOTTOM, pady=50)
        global boutonPlay
        boutonPlay = Button(boutonPlayFrame, text="PLAY", bg = "#dedede", command=motMystere)
        boutonPlay.pack()
    '''
    '''
    def choixNiveau():
        ## Propose les niveaux correspondant au thème selectionné
          # Connexion à la database pour récupérer les thèmes

          # Destruction de la frame niveau au cas où l'utilisateur change de thème
        global mainFenetre
        global niveauFrame
        niveauFrame.destroy()
        global niveau
          # Sélectionne par défaut le premier niveau du thème sélectionné
        niveau = StringVar(value=vwniveau[0][0])
          #Création et affichage de la frame niveau
        niveauFrame = Frame (mainFenetre)
    '''



    #Création et affichage de la frame thème


    mainFenetre.mainloop()


'''
    while (win == False and lost == False):
        ## Tant que le joueur n'a ni gagné, ni perdu, la boucle demande des lettres à l'utilisateur, vérifie si elle est contenue dans le mot mystère et les condition de victoire et défaite
        secret = afficheMotSecret()
        messageErreur, pénalité = chercheLettre()
        if messageErreur != "":
            easygui.msgbox(f"{messageErreur}")
            messageErreur = ""
        secret = afficheMotSecret()
        win = victoire()
        lost = defaite()

'''


## ----- Fonctions Liées au jeu -----

def victoire():
    ## Vérifie si toutes les lettres du mot mystère ont été trouvées et passe le booléen de victoire à True le cas échéant
    victoire = False
    if secret.count("_") == 0:
        victoire = True
        print("Bravo vous avez gagné")
        ## msgbox ("Bravo, vous avez gagné", title = "pendu")
        easygui.msgbox(f"{word}\nBravo, vous avez gagné", "Le Pendu", "Ok !")
    return victoire

def defaite():
    ## Vérifie si le compteur de pénalité a atteint le max et passe le booléen de défaite à True le cas échéant
    defaite = False
    if pénalité == 5:
        defaite = True
        print("Dommage, vous avez perdu")
        easygui.msgbox(f"{word}\nDommage, vous avez perdu", "Le Pendu", "Ok !")
    return defaite

def chercheLettre(n):
    ## Vérifie si la lettre renseignée est dans le mot, l'ajoute dans le tableau de lettres proposées incrémmente le compteur de pénalité le cas échéant
    print('welcome in chercheLettre : ', n)
    global pénalité, lettresProposées, secret, secretLabel
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
            return messageErreur, pénalité
        else:
            print("La lettre est incluse")
            secret = afficheMotSecret()
            try:
                secretLabel.destroy()
            except:
                pass
            secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
            secretLabel.pack()
            secretFrame.pack(side = BOTTOM, pady=20)



## ----- Connexion database -----


def chercheThemeDansDatabase():
    # ----- Etape 3 = Recherche des thèmes dans la database -----
    print('# ----- Etape 3 = Recherche des thèmes dans la database -----')
    global vwtheme
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
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
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
    crs = cnx.cursor()
    crs.execute(f'select * from fx_niveau({t});')
    vwniveau = crs.fetchall()
    crs.close()
    cnx.close()

def chercheMotDansDatabase():
     # ----- Etape 9A = Recherche des mots correspondants au niveau dans la dataBase -----
    print('# ----- Etape 9A = Recherche des mots correspondants au niveau dans la dataBase -----')
    global dataMot
    cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
    crs = cnx.cursor()
    crs.execute(f'select * from fx_mot2({niveau.get()});')
    dataMot = crs.fetchall()
    crs.close()
    cnx.close()



## ----- Fenetre de jeu -----

def creationClavier():
    global clavierFrame, current_lettre
    # ----- Etape 15A = Création de la frame clavier -----
    print('# ----- Etape 15 = Création de la frame clavier et du clavier -----')
    clavierFrame = Frame (mainFenetre, bg = "#dedede")
    # ----- Etape 15B = Création du clavier -----
    print('# ----- Etape 15 = Création de la frame clavier et du clavier -----')
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
    global secretFrame
    secretFrame = Frame(mainFenetre, bg = "#dedede")

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
    # ----- Etape 14 = creation de la frame mot secret -----
    print('# ----- Etape 14 = creation de la frame mot secret -----')
    creationSecretFrame()
    # ----- Etape 15 = Création de la frame clavier et du clavier -----
    print('# ----- Etape 15 = Création de la frame clavier et du clavier -----')
    creationClavier()
    # ----- Etape 15C = Affichage de la frame Clavier -----
    print('# ----- Etape 15C = Affichage de la frame Clavier -----')
    clavierFrame.pack(side = BOTTOM, pady=20)
    # ----- Etape 16 = Création et affichage  de la frame mot secret -----
    print('# ----- Etape 16 = Création et affichage  de la frame mot secret -----')
    secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
    secretLabel.pack()
    secretFrame.pack(side = BOTTOM, pady=20)



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




## ----- Lancement de la fonction jeu -----
pendu()