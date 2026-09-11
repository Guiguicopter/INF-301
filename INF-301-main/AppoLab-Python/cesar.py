texte = """
Gtg,
utzw ijhwduyjw nq kfzy ufwynw ij qf kns iz rjxxflj jy jxxfdjw ij wjkfnwj "f 
q'jsajwx" qjx inkkjwjsyjx jyfujx. Xn yz wjuwjsix q'jcjruqj ij "Ujyny rjxxflj 
htzwy." ts ujzy ufwynw ij qf kns jy wjywtzajw qjx inkkjwjsyx jyfyx ij YCY jy JSH 
ozxvz'fz ijgzy. Ufw jcjruqj xn qj *ijwsnjw* hfwfhyjwj ij JSH jyfny 'f', hjqf 
atziwfny inwj vz'f q'jyfuj uwjhjijsyj ts f qz zs 'f' jy ijuqfhj zs hfwfhyjwj 
f qf kns ij YCY. Js kfnxfsy qjx tujwfyntsx nsajwxjx ts wjywtzaj qj rjxxflj 
nsnynfq
"""

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

print(cesar(texte, -5))