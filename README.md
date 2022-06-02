# jeuPendu


I - Conception du projet

Présentation Générale

Le développement de l’application Pendu est assuré par une équipe de 4 développeurs en mode ”fil rouge“ en parallèle avec l’acquisition des compétences techniques nécessaires.
Il sera codé en Python
les données seront stockées sur une base de données Postgresql


Règles du jeu

L’objectif du pendu est de retrouver un mot “mystère” en découvrant ses lettres.
Déroulement :
 -Les lettres du mot “mystère” s’affichent à l’écran sous forme de _ ou autre symbole
 -Le joueur sélectionne des lettres 1 à 1
-Si la lettre est contenue dans le mot
        -Elle apparaît dans le mot mystère à chaque position où elle est présente
        -Elle se bloque pour ne pas être ré-utilisée
-Si la lettre n’est pas contenue dans le mot
        -On compte une pénalité
        -Elle se bloque pour ne pas être ré-utilisée

-La partie se termine si je joueur atteint xx pénalités ou s’il découvre le mot mystère

