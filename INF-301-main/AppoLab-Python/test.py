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

texte = ""

# for i in range(26):

#     print(cesar(texte, i))
#     print("--------------------------------------", i, "---------------------------------------------")


print(ord('r')%8)
