#!/usr/bin/env python3

from lib.Network import *


class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.associe = valeur
        self.suivant:Noeud = None


class Sequence:
    def __init__(self, noeud : Noeud = None):
        self.tete = noeud
        self.queue = None
        self.longueur = 0
        self.mesurer()
        self.trouver_queue()


    def afficher(self):
        self.mesurer()
        i = 0
        cel = self.tete
        print("sequence :", end=' ')
        if cel:
            while cel and i < self.longueur:
                print(cel.valeur, '~', cel.associe, end = "->")
                cel = cel.suivant
                i+=1
            print(f"=> {cel.suivant.valeur} ~ {cel.suivant.associe}->...")
        print("taille : ", self.longueur)



    def ajoute_debut(self, valeur):
        noeud = Noeud(valeur)
        noeud.suivant = self.tete

        if not(self.tete):
            self.queue = noeud

        self.tete = noeud
        self.queue.suivant = self.tete
        self.longueur += 1

    def ajoute_fin(self, valeur):
        noeud = Noeud(valeur)
    
        if self.queue:
            self.queue.suivant = noeud
        else:
            self.tete = noeud

        noeud.suivant = self.tete
        self.queue = noeud
        self.longueur += 1


    def mesurer(self):
        self.longueur = 0
        cel = self.tete
        if cel:
            self.longueur += 1
            cel = cel.suivant

        while cel and cel!=self.tete:
            self.longueur += 1
            cel = cel.suivant

    def trouver_queue(self):
        if self.longueur == 1:
            self.queue = self.tete
            self.queue.suivant = self.tete
        elif self.tete:
            cel = self.tete
            i = 0
            while cel and i<self.longueur:
                cel = cel.suivant
            self.queue = cel
            self.queue.suivant = self.tete


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

        
        # print(d, sequence, reponse)
    
    return reponse


def crypteAssoc(message):
    seq = Sequence()
    reponse = ""
    for i in message:
        cel = seq.queue
        j = 0
        lettre = ''
        i_dans_seq = False
        while j < seq.longueur and cel and not i_dans_seq:
            if cel.suivant.valeur == i:
                if cel == seq.queue:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe
                    seq.tete = seq.tete.suivant
                    seq.queue = seq.queue.suivant
                    lettre = seq.queue.associe
                    i_dans_seq = True

                elif cel.suivant == seq.queue:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe
                    lettre = seq.queue.associe
                    i_dans_seq = True
                    
                else:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe

                    suivant = cel.suivant
                    cel.suivant = cel.suivant.suivant
                    cel = suivant

                    seq.queue.suivant = cel
                    cel.suivant = seq.tete
                    seq.queue = cel

                    lettre = seq.queue.associe
                    i_dans_seq = True
            else:
                cel = cel.suivant
            j += 1

        if i_dans_seq:
            reponse += lettre
        else:
            seq.ajoute_fin(i)
            reponse += i

        # print(i)
        # print(reponse)
        # seq.afficher()
        # print()
    return reponse

        



def decrypteAssoc(message):
    seq = Sequence()
    reponse = ""
    for i in message:
        cel = seq.tete
        j = 0
        lettre = ''
        i_dans_seq = False
        while j < seq.longueur and cel and not i_dans_seq:
            if cel.associe == i:
                if cel == seq.queue:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe
                    seq.tete = seq.tete.suivant
                    seq.queue = seq.queue.suivant
                    lettre = seq.queue.valeur
                    i_dans_seq = True
    
                elif cel.suivant == seq.queue:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe
                    lettre = seq.queue.valeur
                    i_dans_seq = True
                    
                else:
                    cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe
    
                    suivant = cel.suivant
                    cel.suivant = cel.suivant.suivant
                    cel = suivant
    
                    seq.queue.suivant = cel
                    cel.suivant = seq.tete
                    seq.queue = cel
    
                    lettre = seq.queue.valeur
                    i_dans_seq = True
            else:
                cel = cel.suivant
            j += 1
    
        if i_dans_seq:
            reponse += lettre
        else:
            seq.ajoute_fin(i)
            reponse += i
    
        # print(i)
        # print(reponse)
        # seq.afficher()
        # print()
    return reponse


# abcbcca -> abcabaa
# test = "abcbcca"
# testCrypte = crypteAssoc(test)
# print(testCrypte, '-----------------------------------')
# print(decrypteAssoc(testCrypte))


show_messages(True)

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)
reponseLoad = envoyerRecevoir("load LostCause")
reponseHelp = envoyerRecevoir("help")
reponseStart = envoyerRecevoir("start")
envoyer("tout va bien")

deconnexion()

print(decrypteSeq(reponseHelp))
print("---------------------------------")
print(decrypteAssoc(reponseStart))