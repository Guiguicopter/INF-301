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
        i_dans_seq = False
        while j < seq.longueur and cel and not i_dans_seq: # O(1) car la longueur de seq est 256 au maximum (si le message est en ASCCI exclusivement)

            if cel.suivant.valeur == i:
                i_dans_seq = True # permet d'arreter la boucle while et faire une disjonction de cas plus tard

                # echange les caracteres associes
                cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe

                # if nessecaire pour deffirencier les cas de bords
                if cel == seq.queue:

                    seq.tete = seq.tete.suivant
                    seq.queue = seq.queue.suivant

                elif cel.suivant != seq.queue: 
                    # si cel.suivant == seq.queue il faut juste echanger les valeurs associees ce qui est deja fait avant

                    # -> seq.tete-> ... -> cel -> cel.suivant == suivant -> cel.suivant.suivant -> ... -> seq.queue -> seq.tete
                    suivant = cel.suivant
                    cel.suivant = cel.suivant.suivant
                    # -> seq.tete-> ... -> cel -> cel.suivant.suivant -> ... -> seq.queue -> seq.tete

                    cel = suivant
                    seq.queue.suivant = cel
                    cel.suivant = seq.tete
                    seq.queue = cel
                    # -> seq.tete-> ... -> cel -> cel.suivant.suivant -> ... -> cel.suivant <- seq.queue -> seq.tete

            else:
                cel = cel.suivant
            j += 1

        
        if i_dans_seq:
            reponse += seq.queue.associe
        else:
            seq.ajoute_fin(i)
            reponse += i

        # print(i)
        # print(reponse)
        # seq.afficher()
        # print()
    return reponse

        



def decrypteAssoc(message):
    # la structure et le fonctionnement de decrypteAssoc est le meme que crypteAssoc
    # Seuls les changement seront indiqué
    seq = Sequence()
    reponse = ""
    for i in message:
        cel = seq.tete # changement
        j = 0
        lettre = ''
        i_dans_seq = False
        while j < seq.longueur and cel and not i_dans_seq:
            if cel.associe == i: # changement
                i_dans_seq = True
                
                cel.associe, cel.suivant.associe = cel.suivant.associe, cel.associe

                if cel == seq.queue:
                    seq.tete = seq.tete.suivant
                    seq.queue = seq.queue.suivant
    
                elif cel.suivant != seq.queue:
                    suivant = cel.suivant
                    cel.suivant = cel.suivant.suivant
                    cel = suivant
    
                    seq.queue.suivant = cel
                    cel.suivant = seq.tete
                    seq.queue = cel
    
            else:
                cel = cel.suivant
            j += 1
    
        if i_dans_seq:
            reponse += seq.queue.valeur # changement
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