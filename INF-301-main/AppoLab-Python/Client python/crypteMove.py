#!/usr/bin/env python3

from lib.Network import *



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



show_messages(True)

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"


envoyer("login " + login + " " + mdp)
envoyer("load crypteMove")
message = envoyerRecevoir("help")
envoyer("start")
envoyer(crypter(message))

