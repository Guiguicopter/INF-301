#!/usr/bin/env python3
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!                                                !!!
# !!! Pour démarrer ce programme depuis Idle ou      !!!
# !!! VSCode, faites 'run' depuis le menu (ou        !!!
# !!! touche F5).                                    !!!
# !!!                                                !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!                                                !!!
# !!! Modifications autorisées ci-dessous :          !!!
# !!!                                                !!!
# !!! - login et mdp                                 !!!
# !!! - mode introduction                            !!!
# !!!                                                !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Modifiez les variables ci-dessous: mettez vos identifiant et mot de passe
# /!\ login doit être une `string` (et non un `int`)
login = "12503974"
mdp = "ESTEZET"

# Passez la variable à `False` pour ne plus rejouer l'introduction
# introduction = True
introduction = False



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!          NE PAS MODIFIER CE FICHIER            !!!
# !!!                 CI-DESSOUS                     !!!
# !!!          Vous devez effectuer votre            !!!
# !!!        travail dans client-tutoriel.py         !!!
# !!!         ou dans d'autres fichiers que          !!!
# !!!          vous aurez vous-même créé.            !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!                                                !!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


from lib.Network import *
from time import sleep
from os.path import basename
import argparse

serveur = "im2ag-appolab.u-ga.fr"


def clientInteractif():
    print("""
Ce client est à utiliser pour dialoguer avec AppoLab avec votre clavier.""")
    connexion(serveur)

    show_messages(False)

    sleep(.3)

    if login and mdp:
        print ("Identification avec", login)
        reponse = envoyerRecevoir("login " + str(login) + " '" + mdp + "'")
        color_print(reponse, 'blue')
        sleep(.3)
    else:
        print ("Identifiez vous maintenant en envoyant 'login <identifiant> <mot-de-passe>'")

    while True:
        message = lire_clavier(intro=False)
        reponse = envoyerRecevoir(message)
        color_print(reponse, 'blue')
        sleep(.1)


def clientIntroduction():
    # Affiche les échanges avec le serveur (false pour désactiver)
    show_messages(True)

    print(f"""
    AppoLab est un serveur d'exercices algorithmiques que vous allez devoir
    utiliser pour vos APPs. Je vais vous guider pas à pas pour que vous 
    puissiez vous débrouiller tout·e seul·e.
    Ce client vous permet de discuter de manière interactive (en tapant au
    clavier) avec le serveur AppoLab.""")

    attendre()

    print("""
    Le client va maintenant tenter de se connecter automatiquement au serveur 
    AppoLab. Il vous faut bien entendu pour cela une connection internet.
    (En cas de problème, appellez un enseignant.)""")
    attendre()

    connexion ("im2ag-appolab.u-ga.fr")

    print ("""
    Si tout va bien, vous devez avoir reçu le message de bienvenue d'AppoLab. Si 
    non, arrêtez ce programme (avec Ctrl-C) et demandez de l'aide à un·e 
    enseignant·e.""")

    attendre()

    print ("""
    Comme indiqué, commencez par vous loguer avec l'identifiant et le mot de
    passe qui vous ont été fournis. Pour les étudiants d'INF301, le login est
    votre numéro d'étudiant·e, et le mot de passe votre nom de famille en 
    majuscule.  Entrez les au clavier ainsi :

      login 12345678 \"MOT DE PASSE\"

    (Important: en cas d'espace dans votre nom, mettez bien les guillemets !)""")

    while True:
        login = lire_clavier(intro=True)
        reponse = envoyerRecevoir(login)

        if "Veuillez d'abord" in reponse:
            print ("Vous devez utiliser la commande 'login'")

        elif "incorrect" in reponse:
            print ("Vu avez du vous tromper dans vos identifiants, réessayez...")

        elif "Bienvenue" in reponse:
            break

        else:
            print ("Message inconnu, réessayez de vous loguer...")

    print ("""
    Bravo, vous venez de vous identifier auprès du serveur !
    Comme vous pouvez le voir ce programme trace tout ce que vous envoyez au 
    serveur sur les lignes commençant par <<<envoi<<<, et tout ce que répond le 
    serveur sur des lignes commençant par >>>recu >>>.""")

    attendre()

    print ("""
    Vous êtes maintenant prêt·e à lancer le premier exercice qui se nomme 'tutoriel'.
    Lancez le grâce à la commande 'load' ainsi :
    load tutoriel""")

    while True:
        load = lire_clavier(intro=True)
        reponse = envoyerRecevoir(load)

        if "Commande inconnue" in reponse:
            print ("Vous devez utiliser la commande 'load'")

        elif "n'existe pas" in reponse:
            print ("Vu avez du vous tromper dans le nom de l'exercice, réessayez...")

        elif "Bienvenue" in reponse:
            break

        else:
            print ("Message inconnu, réessayez de vous loguer...")


    print ("""
    Vous venez de lancer votre premier exercice...
    Lisez attentivement les messages reçus du serveur et suivez les consignes 
    de l'exercice à présent.""")

    while True:
        message = lire_clavier(intro=True)
        reponse = envoyerRecevoir(message)

        if "trop lent" in reponse:
            break


    attendre()

    if "c'est trop lent" in reponse:
        print ("""
        Bon, finalement vous avez échoué à cet exercice, mais c'était
        fait exprès :-)""")

        attendre()
        print ("""
        Relancez ce programme et essayez d'être plus rapide cette fois !
        Pour éviter de retaper votre login et mot de passe à chaque fois,
        vous pouvez les renseigner au début de ce fichier
        (client-interactif.py)
        Vous pouvez également désactiver les messages d'introduction en
        passant la variable 'introduction' à False.
        """)

    else:
        print ( """
    Bravo vous êtes plutôt rapide.
    Vous pourriez relancer ce programme pour tenter à nouveau votre
    chance, mais vous allez vite vous rendre compte que c'est fastidieux
    de retaper votre login et mot de passe à chaque fois...""")

        attendre()
        print ("""
    Changez donc de programme et utilisez à la place 'client-tutoriel.py'
    Par contre, vous devez tout d'abord éditer le fichier, et y trouver où 
    rentrer votre identifiant et mot de passe.""")

        attendre()
        print ("Au revoir.")

    deconnexion()
    print ("Fin de la connection au serveur")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--intro', action=argparse.BooleanOptionalAction, default=True)
    args, _ = parser.parse_known_args()

    print ("Bienvenue dans le client interactif d'AppoLab")
    sleep(.3)

    if not introduction or not args.intro:
        print(f"""
    Vous avez lancé le client en mode normal.
    (Pour réactiver le mode 'introduction', passez la variable 'introduction' 
    à True au début de {basename(__file__)})""")

        clientInteractif()
    else:

        print(f"""
    Vous avez lancé le client en mode 'introduction'.
    (Pour désactiver ce mode, passez la variable 'introduction' à False
    au début de {basename(__file__)})""")


        clientIntroduction()
