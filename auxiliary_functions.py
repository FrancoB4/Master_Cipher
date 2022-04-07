from random import randint
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


def save_key(name, key, password, rails):
    with open('./keys.yaml', 'r',  encoding='utf-8') as keys:
        document = yaml.load(keys, Loader=yaml.FullLoader)

        # next_key = len(document['keys'].values())
        new_key = {'key': key, 'password': str(password), 'rails': rails}

        document['keys'][name] = new_key

    with open('./keys.yaml', 'w',  encoding='utf-8') as keys:
        yaml.dump(document, keys, allow_unicode=True)


def new_keys_file():
    with open('./keys.yaml', 'w',  encoding='utf-8') as keys:
        yaml.dump({'keys': {'control': {'working': 'True'}}}, keys, allow_unicode=True)


def use_key(configuration, password):
    password_aux = password[:]
    with open('./keys.yaml', 'r',  encoding='utf-8') as keys:
        document = yaml.load(keys, Loader=yaml.FullLoader)['keys'][configuration]

        if document['password'] == password_aux:
            print('done!')
            return document['key'], document['rails']


def run():
    # testing functions

    # string = 'abcdefghijklmnopqrstuvwxyz!"#$%&/()=?¡{}[]+*-_<>.:,;|°¬´¨`^@~ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # shuffled_string = shuffle_string(string)

    # print(shuffled_string)

    # save('Llave_1', 'Contraseña_1')

    use_key(1, 'contraseña')


if __name__ == '__main__':
    run()
