#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import cleandoc
import socket
import struct
import sys
import argparse

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_STR = "0.1"
VERSION_HEX = 0x01

# To pretend we are an older client, prior to version, uncomment below
# VERSION_MAJOR = 15
# VERSION_MINOR = 15
# VERSION_STR = "15.15"
# VERSION_HEX = 0xff

VERSION = (VERSION_MAJOR, VERSION_MINOR)

BUFLEN=4096

soft_debug_mode = False
hard_debug_mode = False
# soft_debug_mode = True
# hard_debug_mode = True

do_attente_automatique = False

intro_msg = (cleandoc ("""
            ******************************
            *   Bienvenue sur AppoLab    *
            ******************************
            À tout moment, vous pouvez entrer la commande 'aide' ou 'help'
            pour afficher un message d'aide.
            Vous devez tout d'abord vous connecter en utilisant la commande 'login'
            login <identifiant> <mot-de-passe>
            """)+"\n\n")
#
# WARNING: on suppose que le message d'introduction termine toujours par un 
# double retour à la ligne (et pas d'autres lignes vides). C'est ainsi que le 
# client détermine que le message est terminé, avant de passer en mode 
# 'paquets'
#

intro_msglen = len(intro_msg.encode())

SEND = ""
RECV = ""
WAIT = ""

# print error
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


try:
    colorshell = sys.stdout.shell

    # all possible colors in IDLE
    # alls = "SYNC,stdin,BUILTIN,STRING,console,COMMENT,stdout,TODO,stderr,hit,DEFINITION,KEYWORD,ERROR,sel"
    # cols = alls.split(',')
    # for c in cols:
        # colorshell.write ("This is color " + c, c)

    # define colors for IDLE
    SEND = "STRING"
    RECV = "BUILTIN"
    WAIT = "KEYWORD"

    def color_print (message, color, error=False):
        # Will not color print on stderr in IDLE
        colorshell.write(message, color)

except AttributeError:
    # not in IDLE
    try:
        from termcolor import colored

        SEND = "green"
        RECV = "magenta"
        WAIT = "red"

        def color_print (message, color, error=False):
            if error:
                f=sys.stderr
            else:
                f=sys.stdout
            print (colored (message, color), end='', file=f)
    except ImportError:
        def color_print (message, color, error=False):
            if error:
                f=sys.stderr
            else:
                f=sys.stdout
            print (message, end='', file=f)

def prefix_print (prefix, message, color, error=False):
    if message is None:
        color_print (prefix + '<garbage>\n', color, error=error)
        return
    lines = message.split('\n')
    if lines[-1] == "":
        lines.pop()
    for l in lines:
        color_print (prefix + l + '\n', color, error=error)

def prefix_eprint (prefix, message, color):
    prefix_print (prefix, message, color, error=True)

class LanguageError(Exception):
    pass

class ErrorWrite(Exception):
    pass

class PacketModeActivation(Exception):
    pass


class Common:

    def __init__(self, clientsocket, address):
        self.sock = clientsocket
        self.addr = address
        self.str_addr = address[0] + ', ' + str(address[1])

    def settimeout(self, timeout):
        # Note that this python high level interface sets all timeouts:
        # connect, recv and send.
        # Use it:
        # - on clients: either before or after connect
        # - on server: only after accept on the returned client socket
        self.sock.settimeout(timeout)

    def address(self):
        return self.str_addr

    def sendBytes (self, bts):
        self.sock.sendall (bts)

    def sendPacket (self, bts):
        size = len(bts)
        assert size < 0x80000000
        size = socket.htonl(size)
        size = struct.pack('I',size)
        self.sendBytes (size + bts)
        if hard_debug_mode:
            eprint ('size', size)
            eprint ('sent', bts)

    def sendPakString(self, msg):
        bts = msg.encode()
        self.sendPacket (bts)
        if soft_debug_mode:
            prefix_eprint ("<<<envoi<<< ", msg, SEND)

    def sendString(self, msg):
        bts = msg.encode()
        self.sendBytes (bts)
        if soft_debug_mode:
            prefix_eprint ("<<<envoi<<< ", msg, SEND)

    def recvSize (self, size):
        bts = self.sock.recv(size)
        if hard_debug_mode:
            eprint ('recv', bts)

        if not len(bts):
            raise ConnectionResetError

        while len(bts) < size:
            nbts = self.sock.recv (size-len(bts))
            if hard_debug_mode:
                eprint ('recvn', nbts)

            if not len(nbts):
                raise ConnectionResetError
            bts += nbts
        return bts


    def sendCode (self, code):
        code = socket.htonl (code)
        code = struct.pack("I", code)
        self.sendBytes (code)

    def _getCode(self, bt):
        code = struct.unpack('I',bt)[0]
        code = socket.ntohl (code)
        return code

    def recvCode (self):
        bt = self.recvSize(4)
        return self._getCode(bt)

    def recvPacket(self):
        size = self.recvCode ()
        assert not size & 0x80000000  # most significant bit must be 0

        bts = self.recvSize (size)
        return bts

    def _decode(self,msg):
        try:
            msg = msg.decode()
            return msg
        except UnicodeDecodeError:
            # if self.pseudo is None:
            eprint("A client", end=' ')
            # else:
                # print(self.pseudo, file=sys.stderr,end=' ')
            eprint("sent invalid characters to the server")

            if msg == b'\xff\xf4\xff\xfd\x06':
                eprint("Ctrl-C was sent by client")
                self.send("Utilisez plutôt la commande 'quit' que Ctrl-C\n")
            elif msg == b'\xff\xed\xff\xfd\x06':
                eprint("Ctrl-Z was sent by client")
                self.send("Utilisez plutôt la commande 'quit' que Ctrl-Z\n")
            else:
                eprint("First 100 chars:", msg[:100])
                self.send("Invalid string sent\nVerify your program compatibility with UTF-8 characters!\n")

            return None


    def recvString (self):
        msg = self.sock.recv(BUFLEN)
        msg = self._decode(msg)
        if soft_debug_mode:
            prefix_eprint (">>>recu >>> ", msg, RECV)
        return msg


    def recvPakString (self):
        bts = self.recvPacket()
        msg = self._decode(bts)
        if soft_debug_mode:
            prefix_eprint (">>>recu >>> ", msg, RECV)
        return msg

    def disconnect(self):
        self.sock.close()

    def __del__(self):
        del self.sock


PACKET_MASK = 0xFFFF0000
LANGUAGE_MASK = 0x000000FF
VERSION_MASK = 0x0000FF00

PYTHON_HEX = 0x85
C_HEX = 0xCC
CPP_HEX = 0xC8
JAVA_HEX = 0xEA

def create_code(hex_lang, version):
    if version is None:
        ver_hex = VERSION_HEX
    else:
        ver_hex = version_to_hex(version)
    return PACKET_MASK | ver_hex << 8 | hex_lang

def version_from_hex(ver_hex):
    major = ver_hex >> 4
    minor = ver_hex & 0x0F
    return (major, minor)

def version_to_hex(v):
    major, minor = v
    return major << 4 | minor

def version_to_str(v):
    major, minor = v
    return str(major) + '.' + str(minor)

assert version_from_hex(VERSION_HEX) == (VERSION_MAJOR, VERSION_MINOR)
assert version_to_str((VERSION_MAJOR, VERSION_MINOR)) == VERSION_STR

def decode_version(code):
    ver_hex = (code & VERSION_MASK) >> 8
    if ver_hex == 0xFF:
        return (0,0)
    else:
        return version_from_hex(ver_hex)



def flagToLanguage(i):
    if i == CPP_HEX:
        return 'C++'

    if i == PYTHON_HEX:
        return 'python'

    if i == C_HEX:
        return 'C'

    if i == JAVA_HEX:
        return 'java'

    raise LanguageError


TERMBLUE = "\x1B[34m"           # closing bracket ]
TERMBLUEBOLD = "\x1B[34;1m"     # closing bracket ]
TERMRESET = "\x1B[0m"           # closing bracket ]


class NetServer (Common):

    def __init__(self, clientsocket, address):
        self.language = "generic"
        try:
            Common.__init__(self, clientsocket, address)
            self.packet_mode = False
            self.sendString (intro_msg)
        except ConnectionError as e:
            eprint (e)
            eprint ("Erreur à la connexion d'un client")

    def sendColorString(self, msg):
        self.sendString (TERMBLUEBOLD + msg + TERMRESET)

    def recvFirst(self):
        if soft_debug_mode:
            eprint("Receiving first in object", self)
        init = self.recvSize(4)
        code = self._getCode(init)

        if code & PACKET_MASK != PACKET_MASK:
            # not in packet mode
            if soft_debug_mode:
                eprint('Normal mode activated for', self.address())
                eprint('Init was:', init, "for", self.address())
            self.receive = self.recvString
            self.send    = self.sendColorString
            msg = self.recvString()
            if msg:
                msg = init.decode() + msg
            else:
                msg = init.decode()

        else:
            if soft_debug_mode:
                eprint('Packet mode activated for', self.address())
            self.language = flagToLanguage(code & LANGUAGE_MASK)
            self.version = decode_version(code)
            self.packet_mode = True

            if soft_debug_mode:
                eprint('Language detected:', self.language, "for", self.address())
            # send back the code to acknowledge
            self.sendCode (code)

            self.receive = self.recvPakString
            self.send    = self.sendPakString

            msg = self.receive()

        if soft_debug_mode:
            eprint ('Received from:',self.address(), ":", msg)
        return msg

    send = Common.sendString
    receive = recvFirst



class NetClient (Common):

    def __init__(self, address="localhost", port=9999, version=None):

        try:
            sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            Common.__init__(self, sock,(address, port))
            self.sock.connect ((socket.gethostbyname(address), port))
        except ConnectionError as e:
            eprint (e)
            eprint ("Erreur à la connexion, vérifiez l'adresse et le port.")
            eprint ("Peut-être que le serveur a lamentablement planté... ?")
            exit (1)

        try:
            # receive intro message
            intro = self.recvSize (intro_msglen)
            # it is also possible to check that intro ends with \n\n

            code = create_code(PYTHON_HEX, version)

            self.sendCode(code)

            ret = self.recvCode()
            while ret != code:
                ret = self.recvCode()
        except ConnectionResetError as e:
            eprint ("Connexion interrompue par le serveur durant l'initialisation.")
            exit (1)

        print(f"Vous êtes connecté·e au serveur AppoLab {address}")
        if soft_debug_mode:
            prefix_print('>>>recu >>> ', intro.decode(), RECV)

    def send (self, msg):
        try:
            self.sendPakString (msg)
        except (BrokenPipeError, ConnectionResetError) as e:
            eprint ("Connexion interrompue par le serveur durant envoi.")
            exit (1)

    def receive (self):
        try:
            return self.recvPakString()
        except ConnectionResetError as e:
            eprint ("Connexion interrompue par le serveur durant réception.")
            exit (1)
        except Exception as e:
            eprint ("Problème durant la réception. Avez-vous bien suivi les consignes ?")
            exit (1)

    def sendReceive (self, message):
        self.send (message)
        return self.receive ()

    def sendDiscardReturn (self, message):
        self.sendReceive(message)
        return None

    envoyerPur = send
    recevoir = receive

    envoyer = sendDiscardReturn
    envoyerRecevoir = sendReceive
    input = sendReceive

    deconnexion = Common.disconnect
    sendRaw = Common.sendPacket


client_class = None

def connexion (host='im2ag-appolab.u-ga.fr', port=443, version=None):
    """
    Possible to change client version declaration for debug/testing purposes.
    """
    global client_class

    # take arguments from command line if any

    parser = argparse.ArgumentParser(description="AppoLab python client")

    parser.add_argument(
        "--intro",
        action=argparse.BooleanOptionalAction,
        help="(only for compatibility with the client-interactif script)",
    )

    parser.add_argument(
        "--local",
        "-l",
        action=argparse.BooleanOptionalAction,
        help="Connect on local server (for testing purposes)",
    )
    parser.add_argument(
        "idents",
        nargs='*',
        help="Identifiers to use for login."
    )
    args = parser.parse_args()

    if args.local:
        host = 'localhost'
        port = 9999

    if args.idents:
        global login, mdp
        if len(args.idents) != 2:
            print("error: the identifiers must be exactly two (a username and a password)")
            exit(1)
        print ("Setting login and mdp of main module")
        import __main__
        __main__.login, __main__.mdp = args.idents

    client_class = NetClient (host, port, version)

def connexion_test (host='im2ag-appolab.u-ga.fr', port=443, version=None):
    """
    Use this connexion when testing, to avoid problems with argparse
    """
    global client_class
    client_class = NetClient (host, port, version)

def envoyerPur (msg):
    global client_class
    client_class.envoyerPur(msg)

def recevoir ():
    global client_class
    return client_class.recevoir()

def envoyer (msg):
    global client_class
    client_class.envoyer(msg)

def envoyerRecevoir (msg):
    if type(msg) != str: raise ValueError("Le message à envoyer doit être une string")
    envoyerPur (msg)
    msg = recevoir()
    if do_attente_automatique:
        attendre()
    return msg

def deconnexion ():
    global client_class
    client_class.disconnect()

def debug_mode (mode):
    global soft_debug_mode
    soft_debug_mode = mode

debug=debug_mode

show_messages = debug_mode

def attente_automatique (mode):
    global do_attente_automatique
    do_attente_automatique = mode

def sendRaw (msg):
    global client_class
    client_class.sendRaw (msg)

def attendre():
    color_print("--- appuyez sur entree pour continuer ---\n", WAIT)
    input ()


def lire_clavier(intro=False):
    """
    Wait for input given on keyboard.
    If in 'intro'duction mode, does not allow empty messages but instead nudges the user
    to input an actual message on the keyboard.
    Otherwise, return a 'line return' as it is a valid message that is required by some
    exercices (e.g. BraveNewWorld).
    """
    if intro:
        color_print("--- entrez votre message et appuyez sur entree pour continuer ---\n", WAIT)

    nb_empty_messages = 0
    while True:
        try:
            message = input("> ")
        except KeyboardInterrupt:
            print("\nProgramme interrompu.")
            exit(0)
        except EOFError:
            print("\nFin des entrées clavier.")
            exit(0)

        if message != "":
            return message

        if not intro:
            return "\n"

        nb_empty_messages += 1
        if nb_empty_messages > 10:
            print ("Là il faut taper au clavier bande de feignasses !")
        elif nb_empty_messages > 2:
            print ("Vous devez entrer un message au clavier, avez-vous bien lu les consignes ?")
        else:
            print ("Vous devez entrer un message au clavier.")
