#!/usr/bin/env python3

from lib.Network import *

def cesar(cypher, n):
    decyphered = ""

    for i in cypher:
        if ord('a') <= ord(i) and ord(i) <= ord('z'):
            decyphered += chr( (ord(i) - ord('a') + n)%26 + ord('a'))
        elif ord('A') <= ord(i) and ord(i) <= ord('Z'):
            decyphered += chr( (ord(i) - ord('A') + n)%26 + ord('A'))
        else:
            decyphered += i

    return decyphered


# Affiche les messages échangés avec le serveur.
# Mettre à `False` pour désactiver.
show_messages(True)

print("Bienvenue dans le client tutoriel d'AppoLab !")

connexion("im2ag-appolab.u-ga.fr")

# modifiez les lignes ci-dessous en mettant vos identifiants et mot de passe.
# /!\ login doit être une `string` (et non un `int`)
login = "12503974"
mdp = "ESTEZET"

# on envoie des chaînes de caractères prédéfinies au serveur
envoyer("login " + login + " " + mdp)
envoyer("load projetX")

reponse = envoyerRecevoir("help")

envoyer("start")
envoyer("veni vidi vici")

print ("Fin d'envoi des messages.")
print ("Pour envoyer d'autres lignes, ajouter des appels à la fonction `envoyer`")
deconnexion()
print ("Fin de la connection au serveur")

print(cesar(reponse, -5))