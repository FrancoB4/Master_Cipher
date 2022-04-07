from auxiliary_functions import use_key, new_keys_file, save_key
from auxiliary_gui_functions import have_key, create_new_key, copy_new_key, select_configuration, application, show
from master_cipher import MasterCipher


def run():
    # Evalúa si existe un archivo de llaves, en caso de que no, crea uno.
    try:
        open('./keys.yaml', 'r', encoding='utf-8')
    except:
        # Creamos un archivo nuevo de llaves
        new_keys_file()

        # Mostramos una ventana para cargar o crear una llave
        have = have_key()

        # Si tiene una llave, que la introduzca, si no, crearemos una nueva
        if have:
            copy_new_key()
        else:
            create_new_key()

    key, rails = select_configuration()

    encoder = MasterCipher(key, n=rails)

    text, encode = application()

    result = ''

    if encode:
        result = encoder.encode(text)
    else:
        result = encoder.decode(text)

    show(result)


if __name__ == '__main__':
    run()
