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

def pendu():
    '''Lance le pendu'''
    lettresProposées = []
    word=input("Renseignez le mot à deviner").upper()
    secret = []
    global pénalité
    pénalité = 0
    global win
    win = False
    lost = False
    global messageErreur
    messageErreur = ""

    def afficheMotSecret():
        secret = []
        for i in range(len(word)):
            lettreIncluse = False
            for j in range(len(lettresProposées)):
                if lettresProposées[j] == word[i]:
                    lettreIncluse = not lettreIncluse
                else:
                    lettreIncluse = lettreIncluse
            if lettreIncluse == True:
                secret.append(word[i])
                lettreIncluse = not lettreIncluse
            else:
                secret.append("_")
        return secret

    def chercheLettre():
        ## Vérifie si la lettre renseignée est dans le mot
        lettre=input(f"{secret} \n Choisissez une lettre : ").upper()
        messageErreur = ""
        global pénalité
        pénalité = pénalité

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
            if (not letterIsInclude):
                pénalité = pénalité + 1
            return messageErreur, pénalité


    def victoire():
        ## 1 passage de trop
        victoire = False
        if secret.count("_") == 0:
            victoire = True
            print("Bravo vous avez gagné")
            ## msgbox ("Bravo, vous avez gagné", title = "pendu")
            easygui.msgbox(f"{word}\nBravo, vous avez gagné", "Le Pendu", "Ok !")
        return victoire

    def defaite():
        defaite = False
        if pénalité == 5:
            defaite = True
            print("Dommage, vous avez perdu")
            easygui.msgbox(f"{word}\nDommage, vous avez perdu", "Le Pendu", "Ok !")
        return defaite


    while (win == False and lost == False):
        secret = afficheMotSecret()
        messageErreur, pénalité = chercheLettre()
        if messageErreur != "":
            easygui.msgbox(f"{messageErreur}")
            messageErreur = ""
        secret = afficheMotSecret()
        win = victoire()
        lost = defaite()


pendu()