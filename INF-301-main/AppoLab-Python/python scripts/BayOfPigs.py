#!/usr/bin/env python3

from lib.Network import *

def retourner_liste(liste):
    return [liste.pop() for i in range(len(liste))]

def crypter(message):

    messageListe = list(message)
    reponse = ""

    for i in range(len(message)):
        temp = []

        lettre = messageListe.pop(0)
        reponse += lettre
        n = ord(lettre) % 8
        if n < len(messageListe):   
            for j in range(n):
                temp.append(messageListe.pop(0))
        if i==360:
            print(reponse[350:], n, temp)
        messageListe += temp


    return reponse

def decrypter(message):
    reponse = []
    messageListe = list(message)

    for i in range(len(message)):
        temp = []
        lettre = messageListe.pop()
        n = ord(lettre) % 8

        if len(reponse) > n:
            for j in range(n):
                temp.append(reponse.pop())

        temp.append(lettre)

        temp = retourner_liste(temp)
        reponse = temp + reponse

    strReponse = ""
    
    for i in reponse:
        strReponse+=i

    return strReponse




message_crypte = "Pee ct mosusriae.ttg"

print(decrypter(message_crypte))


show_messages(True)

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)

# envoyer("help")
envoyer("load BayOfPigs")
envoyer(crypter("Patria o muerte"))
envoyer("start")

# rep = envoyerRecevoir("start")
# envoyer(decrypter(rep))


rep = envoyerRecevoir("Par otuam eriet")


print ("Fin d'envoi des messages.")
print ("Pour envoyer d'autres lignes, ajouter des appels à la fonction `envoyer`")
deconnexion()
print ("Fin de la connection au serveur")

print(decrypter(rep))