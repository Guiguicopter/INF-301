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

texte = """Erqqh uhsrqvh Dolfh,
>>>recu >>> yrlfl ohv frgh vhfuhwv, dssuhqg-ohv sdu frhxu hw ghwuxlw ohv hqvxlwh srxu soxv 
>>>recu >>> gh vhfxulwh: 5402 2586 9910 4327"""
for i in range(26):

    print(cesar(texte, i))
    print("--------------------------------------", i, "---------------------------------------------")