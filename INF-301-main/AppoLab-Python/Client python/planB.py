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
show_messages(True)

print("Bienvenue dans le client tutoriel d'AppoLab !")

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)
envoyer("load planB")

decalage = 0

reponse = envoyerRecevoir("help")
ligne1 = ""
n=0
l = reponse[n]
while l!='\n':
    ligne1+=l
    n += 1
    l = reponse[n]

for i in range(26):
    temp = cesar(ligne1, i)
    if temp == "Chere Alice," or temp == "Cher Bob,":
        decalage = i

print(cesar(ligne1, decalage), decalage)



envoyer("start")
envoyer("42")
envoyer(cesar("hasta la revolucion", decalage))
# envoyer("")

print ("Fin d'envoi des messages.")
print ("Pour envoyer d'autres lignes, ajouter des appels à la fonction `envoyer`")
deconnexion()
print ("Fin de la connection au serveur")
