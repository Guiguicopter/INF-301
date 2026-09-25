# !/usr/bin/env python3

from lib.Network import *

class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.precedent:Noeud = None
        self.suivant:Noeud = None

class Sequence:
    def __init__(self, noeud : Noeud = None):
        self.tete = noeud
        self.queue = noeud
        self.longueur = 0
        self.mesurer()


    def afficher(self):
        cel = self.tete
        print("liste :", end=' ')
        while cel:
            print(cel.valeur, end = "->")
            cel = cel.suivant
        print("None")
        print("taille : ", self.longueur, '\n')


    def affiche_inverse(self): # affiche de la fin jusqu'au debut
        cel = self.queue
        print("liste :", end=' ')
        while cel:
            print(cel.valeur, end = "->")
            cel = cel.precedent
        print("None")
        print("taille : ", self.longueur, '\n')


    def ajoute_debut(self, valeur):
        noeud = Noeud(valeur)
        noeud.suivant = self.tete
        if self.tete:
            self.tete.precedent = noeud
        else:
            self.queue = noeud
        self.tete = noeud
        self.longueur += 1


    def mesurer(self):
        self.longueur = 0
        cel = self.tete
        while cel:
            self.longueur += 1
            cel = cel.suivant


def decrypteMove(message):
    seq = Sequence()
    mod = 0
    lettre = ''
    for i in range(len(message)):

        lettre = message[-(i+1)]
        mod = ord(lettre) % 8
        # print(mod)

        if i == 0: # initialise le premier element de la sequence
            seq.ajoute_debut(lettre)
            seq.afficher()

        # visualisation de la sequence à l'etape n
                
        # seq.tete -> cel(1) <-> cel(2) <-> ... <-> cel(n-1) <-> cel(n) <- seq.queue avec n > mod

        # pour chaque sequence d'operation je vais mettre en commentaire avant la sequence voulue apres la sequence d'operation
        # le noeud pointe par cel avant la sequence d'operation sera 'cel(i)'
        # le noeud pointe par cel apres la sequence d'operation sera "cel(i)"
        else:
            index=0
            cel = seq.queue

            if mod < seq.longueur:


                if mod == 1:
                    # seq.tete -> 'cel(n)' <-> cel(1) <-> ... <-> cel(n-2) <-> "cel(n-1)" <- seq.queue
                    cel.suivant = seq.tete
                    seq.tete = cel
                    seq.queue = cel.precedent

                else: 
                    # seq.tete -> cel(n-mod+1) <-> ... <-> 'cel(n)' <-> cel(1) <-> ... <-> "cel(n-mod-1)" <-> cel(n-mod) <- seq.queue
                    while index <= mod and cel:
                        if index == 0:
                            # <-> 'cel(n)' <- seq.queue <- seq.tete -> cel(1) <-> ... <-> cel(n-2) <-> "cel(n-1)" <->
                            cel.suivant = seq.tete
                            seq.tete.precedent = cel
                            cel = cel.precedent

                        elif index == mod-1:
                            # <-> seq.tete -> 'cel(n-mod+1)' <-> ... <-> cel(n) <- seq.queue <- cel(1) <-> ... <-> cel(n-mod-1) <-> "cel(n-mod)" <->
                            seq.tete = cel
                            cel = cel.precedent

                        elif index == mod:
                            # <-> seq.tete -> cel(n-mod+1) <-> ... <-> cel(n) <- cel(1) <-> ... <-> "cel(n-mod-1)" <-> 'cel(n-mod)' <- seq.queue
                            seq.queue = cel
                            cel = cel.precedent

                        else: # si 0 < index < mod-1
                            cel = cel.precedent

                        index += 1

                if seq.tete.suivant: # evite une erreur
                    seq.tete.suivant.precedent = seq.tete

            # <-> seq.tete -> cel(n-mod+1) <-> ... <-> cel(n) <- cel(1) <-> ... <-> cel(n-mod-1) <-> cel(n-mod) <- seq.queue
            # seq.tete.precedent = seq.queue
            seq.queue.suivant = None
            # seq.queue <- seq.tete -> cel(n-mod+1) <-> ... <-> cel(n) <- cel(1) <-> ... <-> cel(n-mod-1) <-> cel(n-mod) <- seq.queue -> None
            
            seq.ajoute_debut(lettre)
            # seq.affiche_inverse()

    # seq.afficher()
    # la fin transforme la sequence en chaine de caractere
    reponse = ""
    cel = seq.tete

    while cel:
        reponse += cel.valeur
        cel = cel.suivant
    return reponse



# crypte = "Pee ct mosusriae.ttg"
# print(decrypteMove(crypte))



show_messages(True)

connexion("im2ag-appolab.u-ga.fr")

login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)
reponse = envoyerRecevoir("load OneMillion")
# print(decrypteMove(reponse))


bulk = envoyerRecevoir("help")
clef = envoyerRecevoir("start")

reponse = envoyerRecevoir(decrypteMove(bulk*9999+clef)[:100])
print(reponse)
print(decrypteMove(reponse))

deconnexion()

