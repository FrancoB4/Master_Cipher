import sys
import yaml
import PySimpleGUI as psg
from random import choice
from typing import Tuple
from .functions import save_key, use_key, new_keys_file


def have_configuration() -> bool:
    """If there isn't any key file, creates a window where the user is asked if they have a key and want to import it.

    Returns:
        bool: True if user has a key, False if they hasn´t.
    """

    window = psg.Window('Bienvenido', [
        [psg.Text('Tienes una llave de cifrado?')],
        [psg.Radio('Si', 1), psg.Radio('No', 1, default=True)],
        [psg.Ok(), psg.Cancel()]
    ])
    event, values = window.read()
    window.close()

    if event == 'Cancel':
        # Confirm window in future
        sys.exit()

    return values[0]


def set_configuration_params(path: str) -> None:
    """Creates a window where the user can create a new encoder configuration. After that, save it in the keys file

    Args:
        path (str): the specific path of the keys file.
    """
    
    key = ''

    window = psg.Window('Creando una nueva configuración', [
        [psg.Text('Cual sera el nombre de esta configuración?')],
        [psg.Input()],
        [psg.Text('\nDefina el tamaño deseado de la nueva llave (recomendado >50)')],
        [psg.Input()],
        [psg.Text('\nNumero de rieles de cifrado de la configuración\nNúmeros mas bajos funcionan mejor en textos '
                  'cortos\n(recomendado 6)')],
        [psg.Slider((3, 15), orientation='horizontal', default_value=25)],
        [psg.Text('\nCree una contraseña para la configuración (recuérdela bien)')],
        [psg.Input()],
        [psg.Ok(), psg.Cancel()]
    ])

    event, values = window.read()
    window.close()

    if event == 'Cancel':
        # Confirm window in future
        sys.exit()

    name = values[0]
    length = int(values[1])
    rails = int(values[2])
    password = values[3]

    for _ in range(length):
        key += choice('abcdefghijklmnopqrstuvwxyz!"#$%&/()=?¡{}[]+*-_<>ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    save_key(path, name, key, password, rails)


def import_configuration(path: str) -> None:
    """If the user want to importe a new key, this function creates a window where they can do it. After that, save it
    on the keys file.

    Args:
        path (str): the specific path of the keys file.
    """

    window = psg.Window('Importando una configuración', [
        [psg.Text('Cual sera el nombre de esta configuración?')],
        [psg.Input()],
        [psg.Text('\nIngrese su llave de cifrado')],
        [psg.Input()],
        [psg.Text('\nNumero de rieles de cifrado de la configuración\nNúmeros mas bajos funcionan mejor en textos '
                  'cortos\n(recomendado 6)')],
        [psg.Slider((3, 15), orientation='horizontal', default_value=6)],
        [psg.Text('\nCree una contraseña para la configuración (recuérdela bien)')],
        [psg.Input()],
        [psg.Ok(), psg.Cancel()]
    ])

    event, values = window.read()
    window.close()

    if event == 'Cancel':
        # Confirm window in future
        sys.exit()

    name = values[0]
    key = values[1]
    rails = int(values[2])
    password = values[3]

    save_key(path, name, key, password, rails)


def create_new_key(path: str) -> Tuple[str, int]:
    """Creates a new key from the select configuration menú.

    Args:
        path (str): The path of the keys file

    Returns:
        Tuple[str, int]: The key and the rails of the selected configuration.
    """

    have = have_configuration()

    if have:
        import_configuration(path)
        return select_configuration(path)
    else:
        set_configuration_params(path)
        return select_configuration(path)


def select_configuration(path: str) -> Tuple[str, int]:
    """Creates a window where user will select the target configuration. They must insert the password of the
    configuration. If the user insert wrong password 3 times, delete the old keys file and creates new one.

    Args:
        path (str): the specific path of the keys file.

    Returns:
        Tuple[str, int]: return the selected key and rail (necessary to encode and decode) to instantiate
                            a MasterEncoder class.
    """

    configs = []

    with open(path, 'r', encoding='utf-8') as doc:
        document = yaml.load(doc, Loader=yaml.FullLoader)['keys']
        for config in document.keys():
            configs.append(config)

    # The bucle will continue up to three times if the user insert a wrong password
    # When they inset de correct one, return the key and n rails and end the function
    for i in range(3):
        window = psg.Window('Selección de configuración', [
            [psg.Text('Seleccione una configuración:')],
            [psg.Combo(configs, default_value='default')],
            [psg.Text('\nIntroduzca la contraseña de la configuración')],
            [psg.Input()],
            [psg.Ok(), psg.Cancel(), psg.Button('New')]
        ])

        event, values = window.read()
        window.close()

        if event == 'New':
            return create_new_key(path)
        elif event == 'Cancel':
            # Confirm window in future
            sys.exit()
        else:
            try:
                key, rails = use_key(path, values[0], values[1])
                return key, rails
            except TypeError:
                psg.Popup('Wrong password', text_color='red', button_color=(
                    'red', 'white'), background_color='black')
                continue

    # Overwrite the keys file if the user insert three wrong passwords
    new_keys_file(path)
    psg.Popup('Se han realizado demasiados intentos erroneos, por seguridad se eliminaran las'
              'configuraciones guardadas')
    sys.exit()


def application() -> Tuple[str, bool]:
    """Creates the main window of the program, where the user can encode or decode any text.

    Returns:
        Tuple[str, bool]: The str is the resul of encode or decode the user input. The bool will be True
                            if the user checks the encode box and False if checks the decode box.
    """

    window = psg.Window('Master Encoder', [
        [psg.Text('Ingrese el texto')],
        [psg.Input(size=(20, 20))],
        [psg.Radio('encode', 1, default=True), psg.Radio('decode', 1)],
        [psg.Ok(), psg.Cancel()],
    ])

    event, values = window.read()
    window.close()
    if event == 'Cancel':
        # Conform window in future
        sys.exit()

    return values[0], values[1]


def show(res: str) -> bool:
    """Creates a window to show the result of the encode/decode operation. Here the user can re-run the
    main window (application()), close the program or select a new encoder configuration.

    Args:
        res (str): the result of the encoding or decoding.

    Returns:
        bool: True if the user press the button 'Ok' and False in any other case.
    """

    window = psg.Window('Resultados', [
        [psg.Text('El resultado de la operación es: ')],
        [psg.Input(default_text=res)],
        [psg.Ok(), psg.Cancel(), psg.Button('Change Configuration')]
    ])

    event, _ = window.read()
    window.close()

    if event == 'Ok':
        return True
    elif event == 'Change Configuration':
        psg.Popup('Coming soon!')
        return False
    else:
        psg.Popup('Bye!')
        return False
