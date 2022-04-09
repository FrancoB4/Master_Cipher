from random import randint
from typing import Tuple
import yaml


def shuffle_string(string: str) -> str:
    """Shuffle a string randomly

    Args:
        string (str): The string to shuffle

    Returns:
        str: The shuffled string
    """

    shuffled_string = list(string[:])
    longitud_lista = len(shuffled_string)
    for i in range(longitud_lista):
        indice_aleatorio = randint(0, longitud_lista - 1)
        temporal = shuffled_string[i]
        shuffled_string[i] = shuffled_string[indice_aleatorio]
        shuffled_string[indice_aleatorio] = temporal
    return ''.join(shuffled_string)


def save_key(path: str, name: str, key: str, password: str, rails: int) -> None:
    """Saves an encoder config in the keys file.

    Args:
        path (str): The path of the keys file;
        name (str): The name of the configuration;
        key (str): The key of the configuration;
        password (str): The password of the configuration;
        rails (int): The number of rail used to encode user´s texts. (See how it works in 
                        rail_fence_cipher documentation)
    """

    with open(path, 'r', encoding='utf-8') as keys:
        document = yaml.load(keys, Loader=yaml.FullLoader)

        new_key = {'key': key, 'password': str(password), 'rails': rails}

        document['keys'][name] = new_key

    with open(path, 'w', encoding='utf-8') as keys:
        yaml.dump(document, keys, allow_unicode=True)


def new_keys_file(path: str):
    """Creates a new keys file or overwrite the old one.

    Args:
        path (str): The path of the keys file.
    """

    with open(path, 'w', encoding='utf-8') as keys:
        yaml.dump({'keys': {'default': {'key': 'NH$$my=%")CKX&+%X[FMMjeH[$/L¡Hi=EB}c+TavN¡"uIpe$¡XT*_/oL(Np/Ao<u!$&L)(',
                                        'password': 'default', 'rails': 6}}}, keys, allow_unicode=True)


def use_key(path: str, configuration: str, password: str) -> Tuple[str, int]:
    """Reads the keys file and load some encoder configuration.

    Args:
        path (str): The path of the keys file.
        configuration (str): The name of the configuration.
        password (str): The inserted password to try on the configuration.

    Returns:
        Tuple (str, int): if the password is correct, the key of the configuration and the number of rails.
    """

    password_aux = password[:]
    with open(path, 'r', encoding='utf-8') as keys:
        document = yaml.load(keys, Loader=yaml.FullLoader)['keys'][configuration]

        if document['password'] == password_aux:
            print('done!')
            return document['key'], document['rails']


def run():
    pass
    # testing functions

    # string = 'abcdefghijklmnopqrstuvwxyz!"#$%&/()=?¡{}[]+*-_<>.:,;|°¬´¨`^@~ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # shuffled_string = shuffle_string(string)

    # print(shuffled_string)

    # save('Llave_1', 'Contraseña_1')

    # use_key(1, 'contraseña')


if __name__ == '__main__':
    run()
