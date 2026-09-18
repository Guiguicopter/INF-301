# def cesar(cypher, n):
#     decyphered = ""

#     for i in cypher:
#         if ord('a') <= ord(i) and ord(i) <= ord('z'):
#             decyphered += chr( (ord(i) - ord('a') + n)%26 + ord('a'))
#         elif ord('A') <= ord(i) and ord(i) <= ord('Z'):
#             decyphered += chr( (ord(i) - ord('A') + n)%26 + ord('A'))
#         else:
#             decyphered += i

#     return decyphered

# texte = ""

# # for i in range(26):

# #     print(cesar(texte, i))
# #     print("--------------------------------------", i, "---------------------------------------------")


# print(ord('r')%8)


def retourner_liste(liste):
    return [liste.pop() for i in range(len(liste))]



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

message = """Aiesoi di
c mselie
, anne ma pu Blustdsuo bee s.sogoocen nev voab.Dto"""

print(decrypter(message))