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

def crypteSeq(message):
    sequence = []
    reponse = ""

    for i in message:
        d = ''
        is_i_in_sequence = False
        j = 0

        while j < len(sequence) and not(is_i_in_sequence):
            # print(j, len(sequence))
            if i == sequence[j]:
                d = sequence[j-1]
                tmp = sequence.pop(j)
                is_i_in_sequence = True
            j += 1

        if not(is_i_in_sequence):
            reponse += i
            sequence.append(i)
        else:
            reponse += d
            sequence.append(tmp)
        
        
        # print(d, sequence, reponse)
        
    
    return reponse

def decrypteSeq(message):
    reponse = ""
    sequence = []

    for i in message:
        d = ''
        tmp = ''
        is_i_in_sequence = False
        j = 0

        while j < len(sequence) and not(is_i_in_sequence):
            # print(j, len(sequence))
            if i == sequence[j]:
                d = sequence[(j+1) % len(sequence)]
                tmp = sequence.pop((j+1) % len(sequence))
                is_i_in_sequence = True
            j += 1

        if not(is_i_in_sequence):
            sequence.append(i)
            reponse += i
        else:
            reponse += d
            sequence.append(tmp)

        
        print(d, sequence, reponse)
    
    return reponse



message = "hasta la victoria siempre"
print(crypteSeq(message))

show_messages(True)

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)
envoyer("load crypteSeq")
message = envoyerRecevoir("start")

reponse = envoyerRecevoir(crypteSeq(decrypter(message)))

deconnexion()

print(reponse)
