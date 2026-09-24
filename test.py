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


    def affiche_inverse(self):
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
    for i in range(len(message)):

        lettre = message[-(i+1)]
        mod = ord(lettre) % 8
        # print(mod)

        if i == 0:
            seq.ajoute_debut(lettre)
            # seq.afficher()

        else:
            index=0
            cel = seq.queue
            tete = seq.tete
            queue = seq.queue

            if mod < seq.longueur:
                if mod == 1:
                    cel.suivant = seq.tete
                    tete = cel
                    queue = cel.precedent

                else:

                    while index <= mod and cel:

                        if index == 0:
                            cel.suivant = seq.tete
                            seq.tete.precedent = cel
                            cel = cel.precedent

                        elif index == mod-1:
                            tete = cel
                            cel = cel.precedent

                        elif index == mod:
                            queue = cel
                            cel = cel.precedent

                        else:
                            cel = cel.precedent

                        index += 1

                seq.queue = queue
                seq.tete = tete
                if seq.tete.suivant:
                    seq.tete.suivant.precedent = seq.tete


            seq.tete.precedent = queue
            seq.queue.suivant = None
            seq.ajoute_debut(lettre)
            # seq.affiche_inverse()

    # seq.afficher()
    reponse = ""
    cel = seq.tete

    while cel:
        reponse += cel.valeur
        cel = cel.suivant
    return reponse



crypte = "Bob, mon message BgBtr,uvsBdm,gel'milv.sLan--,smo'p-nlBoLg-d"
print(decrypteMove(crypte))


