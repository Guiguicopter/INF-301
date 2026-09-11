#!/usr/bin/env python3

from lib.Network import *

show_messages(True)

print("Bienvenue dans le client tutoriel d'AppoLab !")

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)



print ("Fin d'envoi des messages.")
print ("Pour envoyer d'autres lignes, ajouter des appels à la fonction `envoyer`")
deconnexion()
print ("Fin de la connection au serveur")
