from Scripts.auxiliary.gui_builder import *
from Scripts.classes.master_cipher import MasterCipher

PATH = './keys.yaml'


def run():
    # Evalúa si existe un archivo de llaves, en caso de que no, crea uno.
    try:
        open(PATH, 'r', encoding='utf-8')
    except:
        # Creamos un archivo nuevo de llaves
        new_keys_file(PATH)

        # Mostramos una ventana para cargar o crear una llave
        have = have_key()

        # Si tiene una llave, que la introduzca, si no, crearemos una nueva
        if have:
            copy_new_key(PATH)
        else:
            create_new_key(PATH)

    # Abrimos la pestaña para cargar una configuración
    key, rails = select_configuration(PATH)

    # Abrimos la pestaña principal de la aplicación, y retornamos los valores ingresados
    # Para que la ejecución no termine a la primera vez, creamos un bucle
    while True:
        # Creamos un objeto que instancie el encriptador
        encoder = MasterCipher(key, n=rails)
        text, encode = application()

        if encode:
            result = encoder.encode(text)
        else:
            result = encoder.decode(text)

        keep_encoding = show(result)

        if keep_encoding:
            pass
        else:
            break

    print('All works very well, keep improving')


if __name__ == '__main__':
    run()
