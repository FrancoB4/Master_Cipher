import yaml
import PySimpleGUI as psg
from random import choice
from auxiliary_functions import save_key, use_key, new_keys_file


def have_key() -> bool:
    window = psg.Window('Bienvenido', [
        [psg.Text('Tienes una llave de cifrado?')],
        [psg.Radio('Si', 1), psg.Radio('No', 1, default=True)],
        [psg.Ok(), psg.Cancel()]
    ])
    event, values = window.read()
    window.close()

    return values[0]


def create_new_key():
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
    name = values[0]
    length = int(values[1])
    rails = int(values[2])
    password = values[3]

    for _ in range(length):
        key += choice('abcdefghijklmnopqrstuvwxyz!"#$%&/()=?¡{}[]+*-_<>ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    save_key(name, key, password, rails)


def copy_new_key():
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
    name = values[0]
    key = values[1]
    rails = int(values[2])
    password = values[3]

    save_key(name, key, password, rails)


def select_configuration() -> (str, int):
    configs = []

    with open('./keys.yaml', 'r', encoding='utf-8') as doc:
        document = yaml.load(doc, Loader=yaml.FullLoader)['keys']
        for config in document.keys():
            configs.append(config)

    window = psg.Window('Selección de configuración', [
        [psg.Text('Seleccione una configuración:')],
        [psg.Combo(configs[1:], default_value='seleccione una')],
        [psg.Text('\nIntroduzca la contraseña de la configuración')],
        [psg.Input()],
        [psg.Ok(), psg.Cancel()]
    ])

    for i in range(3):
        event, values = window.read()
        window.close()
        print(values[0])
        try:
            key, rails = use_key(values[0], values[1])
            return key, rails
        except KeyError as ke:
            psg.Popup(ke, text_color='red', button_color=('red', 'white'), background_color='black')
            break

    new_keys_file()
    psg.Popup('Se han realizado demasiados intentos erroneos, por seguridad se eliminaran las'
              'configuraciones guardadas')


def application():
    window = psg.Window('Master Encoder', [
        [psg.Text('Ingrese el texto')],
        [psg.Input(size=(20, 20))],
        [psg.Radio('encode', 1, default=True), psg.Radio('decode', 1)],
        [psg.Ok(), psg.Cancel()],
    ])

    event, values = window.read()
    window.close()

    return values[0], values[1]


def show(res):
    window = psg.Window('Resultados', [
        [psg.Text('El resultado de la operación es: ')],
        [psg.Input(default_text=res)],
        [psg.Ok(), psg.Cancel()]
    ])

    _ = window.read()
    window.close()

    psg.Popup('Adios!')
