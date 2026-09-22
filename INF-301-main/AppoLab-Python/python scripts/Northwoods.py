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

        
        # print(d, sequence, reponse)
    
    return reponse

show_messages(True)

connexion("im2ag-appolab.u-ga.fr")


login = "12503974"
mdp = "ESTEZET"

envoyer("login " + login + " " + mdp)
envoyer("load Northwoods")
envoyer("start")
reponse = envoyerRecevoir("hasta la victoria siempre")

reponseDecryptee = decrypteSeq(reponse)
motDePasseTemporaire = ""
ecrire = False
n=0
for i in reponseDecryptee:
    if i == '\'':
        ecrire = not(ecrire)
        n+=1
    elif ecrire == True and n==3:
        motDePasseTemporaire += i

reponse = envoyerRecevoir(motDePasseTemporaire)

reponse = envoyerRecevoir(crypteSeq("There will be no Nineteen Eighty-Four"))

deconnexion()

# print(motDePasseTemporaire)
# print(decrypteSeq(reponse))
print(reponse)

reponse = """BOO,
Je viJnsJdisrdpr ppdspnractvJtcdddndnpevvvaveupeJoiuiudpucleJrlrumosrp rsn u.,Tmepct umdsqTccsurTuiTgosfncBagtmpi,ordvartprpunrrsrdsAJts.u'ueavrv'qsecnAsasad'v,pu'Aujclmjvxjarc
ptxxAx
a'TpcrotfAeimx irusclsimsssnrlqi
sumjjral e
riiaelnavtsrrmuau"g,qnjll ljffaupi'""junfxt fa,nCpqn.pcf
"CaJuuoddclienol saq
ul p'ardprjdrffifeece.Dm
"iD-fpu.sai
dTii"giq
gpexLmn
"dioc n"C'g'sqaDimAlvfgCepvCr'd
dIc.qgslcssoeradaLsracfft"oCnIe'sarcreo
olfCtfnctTofqluo,xq,ssbnanlqtaii-ollsssren,iIpqmpocvaIdl'qfmuemunaiiecr-tbcehudnjLoyjimStI myg
C'aSruld
p 
 ovl.Bqc,q'cp.SSrrjouSduSfq'aScplsdr lfffcnurpolr   rr'nu
drqqiuqduiphiilhcsg
qeidfieoraySsSu.nSmreSsaoagJiijlJ'mmmmmtullims
lnedfmliJst ggiiig-rm
jgqod qdqs.nC
pJhlgJcluCao aqJCria'hsiigufqsnqlOct-dNvwWLB
q Cs.CN.aBuueJievj oills
ayc ytyorrqrqieeWuov,erWucWl.tJJuurdu'seeuesuosnhlJ'iibJdtnymmWrW'isWyrbdueihmdsebygmr'uWajJ.nvl irrtWagtattCidoss
gm'iImgcva,mnnmup,,,mojSesirpribfJrpbbsybrGgtWWtlej'Sdirttaddbtd nnm tdhor,t'fduhvtvditrzDhpaftSvr-do-GGFTDgsFUSPjAIAVFOES!."""

print(decrypteSeq(reponse))