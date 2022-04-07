from rail_fence_cipher import RailFenceCipher
from vigenere_cipher import VigenereCipher


class MasterCipher:
    rail_encoder = None
    vigenere_encoder = None
    keydict = {}
    key = ''
    alphabet = ''
    n = 0

    def __init__(self, key: str, n: int = 3, alphabet: str = '(lcCF#Yid¬E)RNL<[?*uh/vs`g}@p|V>]fk¨,'
                                                             'AaODXU+Q^joe~BW$¡b-qPIG_.T°{yzZ&KM!J=´Hm:n"tw%;xrS'):
        self.alphabet = alphabet*2
        self.key = key
        self.keydict = {char: self.alphabet.index(char) for char in self.key}
        self.rail_encoder = RailFenceCipher()
        self.vigenere_encoder = VigenereCipher(key, alphabet=self.alphabet)
        self.n = n

    def encode(self, text: str) -> str:
        rail_encoded_text = self.rail_encoder.encode(text, self.n)
        complete_encode_text = self.vigenere_encoder.encode(rail_encoded_text)

        return complete_encode_text

    def decode(self, text: str) -> str:
        vigenere_decoded_text = self.vigenere_encoder.decode(text)
        complete_decode_text = self.rail_encoder.decode(
            vigenere_decoded_text, self.n)

        return complete_decode_text
