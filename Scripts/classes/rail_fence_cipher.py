import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class RailFenceCipher:
    rails = []
    n_str = ''
    cont = ''
    result = ''

    def __init__(self) -> None:
        pass

    def encode(self, string: str, n) -> str:
        self.rails = [[] for _ in range(n)]
        self.n_str = ''
        self.cont = ''
        self.result = ''
        
        for i in range(1, n + 1):
            self.n_str += str(i)

        self.n_str += self.n_str[::-1][1:-1]

        while len(self.cont) < len(string):
            self.cont += self.n_str

        for i, char in enumerate(string):
            self.rails[int(self.cont[i]) - 1].append(char)

        for rail in self.rails:
            self.result += ''.join(rail)

        if len(self.result) != len(self.result.strip()):
            self.dif = len(self.result) - len(self.result.strip())
            self.result = self.result.strip()
            for i in range(self.dif):
                self.result += '_'
        
        return self.result

    def decode(self, string: str, n: int) -> str:
        self.rails = []
        self.n_str = ''
        self.count = {}
        self.result = ''

        for i in range(1, n + 1):
            self.n_str += str(i)

        self.n_str += self.n_str[::-1][1:-1]

        while len(self.n_str) < len(string):
            self.n_str += self.n_str

        if len(self.n_str) > len(string):
            n_str = self.n_str[:len(string)]

        for i in self.n_str:
            try:
                self.count[i] += 1
            except KeyError:
                self.count[i] = 1

        for i in self.count.values():
            self.rails.append([k for k in string[:i]])
            string = string[i:]

        for i in self.n_str:
            self.result += self.rails[int(i) - 1][0]
            self.rails[int(i) - 1].pop(0)

        return self.result.replace('_', ' ')


def run():
    encoder = RailFenceCipher()
    
    rails = int(input('Rieles de cifrado deseados: '))
    
    enc_or_denc = int(input('¿Desea cifrar [0] o descifrar [1] un texto?: '))
    
    if enc_or_denc == 0:
        text_to_encode = input('Ingrese el texto a cifrar:\n')
        print('Su texto cifrado es:\n' + encoder.encode(text_to_encode, rails))
    elif enc_or_denc == 1:
        text_to_decode = input('Ingrese el texto a descifrar:\n')
        print('Su texto descifrado es:\n' + encoder.decode(text_to_decode, rails))
    else:
        logger.info('Valor introducido invalido... reseteando programa')
        run()


if __name__ == '__main__':
    run()
