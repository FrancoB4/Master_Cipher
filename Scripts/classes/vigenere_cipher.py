import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class VigenereCipher(object):
    keydict = {}
    key = ''
    alphabet = ''
    control = ''
    resulte = ''
    resultd = ''

    def __init__(self, key: str,
                 alphabet: str = 'abcdefghijklmnopqrstuvwxyz!"#$%&/()=?¡{}[]+*-_<>.:,'
                                 ';|°¬´¨`^@~ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.alphabet = alphabet * 2
        self.key = key
        self.keydict = {char: self.alphabet.index(char) for char in self.key}

    def encode(self, text: str):
        self.resulte = ''
        while len(self.control) < len(text):
            self.control += self.key
        try:
            textdice = {char: (self.alphabet.index(char) if char in self.alphabet else 0) for char in text}
        except ValueError:
            return text

        for i, char in enumerate(text):
            if char in self.alphabet:
                self.resulte += self.alphabet[textdice[char] + self.keydict[self.control[i]]]
            else:
                self.resulte += char
        return self.resulte

    def decode(self, text: str):
        self.resultd = ''
        while len(self.control) < len(text):
            self.control += self.key
        try:
            textdicd = {char: (self.alphabet.index(char) if char in self.alphabet else 0) for char in text}
        except ValueError:
            return text
        for i, char in enumerate(text):
            if char in self.alphabet:
                self.resultd += self.alphabet[textdicd[char] - self.keydict[self.control[i]]]
            else:
                self.resultd += char
        return self.resultd


def run():
    key = input('Ingrese la llave de cifrado: ')
    alphabet = input('Ingrese su alfabeto [Deje este campo vacio para utilizar el alfabeto por defecto]:\n')
    if alphabet == '':
        encoder = VigenereCipher(key)
    else:
        encoder = VigenereCipher(key, alphabet)

    enc_or_denc = int(input('¿Desea cifrar [0] o descifrar [1] un texto?: '))

    if enc_or_denc == 0:
        text_to_encode = input('Ingrese el texto a cifrar:\n')
        print('Su texto cifrado es:\n' + encoder.encode(text_to_encode))
    elif enc_or_denc == 1:
        text_to_encode = input('Ingrese el texto a descifrar:\n')
        print('Su texto descifrado es:\n' + encoder.decode(text_to_encode))
    else:
        logger.info('Valor introducido invalido... reseteando programa')
        run()


if __name__ == '__main__':
    run()
