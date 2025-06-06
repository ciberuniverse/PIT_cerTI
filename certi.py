from hashlib import md5
from json import loads
from sys import argv
import os
import requests

TERMINAL = False
FILE_CODE = None
DOMAIN_HOST = "http://127.0.0.1:5000/solve"

params_ = ["--check", "--solve"]
all_dirs = os.listdir(".")

# Esto busca el archivo a escanear dentro de la carpeta de manera semantica
for x in all_dirs:

    if "certificacion_" in x:
        FILE_CODE = x
        """Esta variable se rellena usando el nombre de tu archivo que estas programando"""
        break

if not FILE_CODE:
    print("[ERROR] No estas ejecutando el archivo desde la carpeta de certificacion tecnica.")
    exit(0)

RESP_SOLVE = None
"""Esta variable deberia de contener tu respuesta codificada en str"""

ID = None
"""Esta variable es OBLIGATORIA debe contener tu ID dada en el test tecnico"""

usage_ = """
Uso: 
    ceri.py --check|send -R <tu_archivo_de_respuestas> -ID <ID_Proporcionada_en_cerTI>

Ejemplo:
    certy.py --check -R respuestas.txt -ID PIT:d5098d199d0de6dacc877537cf6aab28
    certy.py --solve -R respuestas.txt -ID PIT:d5098d199d0de6dacc877537cf6aab28

--check: Realiza una validacion de tu respuesta comparando las respuestas esperadas
         localmente para verificar tus respuestas.

--solve: Envia las respuestas a los servidores para su validacion y si corresponde
         entrega del certificado.

:: ADVERTENCIA :: Se realizaran verificaciones constantes por cada ejercicio y certificado
entregado, en caso de que se verifique el intento de engaño, o falta al sistema de verificacion
se realizara una suspencion que quedara a criterio del evaluador.
"""


def check_semantic(permitido: list, denegado: list) -> bool:
    """Se valida que la semantica del codigo este escrita correctamente."""

    def show_sc(elem_: str) -> None:
        """Funcion para ser usada en map, solamente imprime en pantalla"""
        print(f"    - {elem_}")

    def map_art(func, iterable: list) -> None:
        """Map artesanal para tener mas legibilidad sin for"""    
        for elem in iterable:
            func(elem)
    
    try:
        with open(FILE_CODE, "r", encoding="UTF-8") as read_code:

            file_ = read_code.read()

            allow = []
            deny = []

            for x in permitido:

                if x not in file_:
                    allow.append(x)

            if allow:
                print(f":: Vas por buen camino, sin embargo no estas cumpliendo con el criterio de evaluacion ::\n:: NO ESTAS USANDO ::")
                map_art(show_sc, allow)
                return False
            
            for x in denegado:
                
                if x in file_:
                    deny.append(x)
            
            if deny:
                print(f":: Todo bien, pero no puedes utilizar las siguientes sentencias ::\n:: ESTAS USANDO ::")
                map_art(show_sc, deny)
                return False
            
        return True
    
    except Exception as err:
        print(f"[ERROR] {err}")
        return False

def valid_():

    params = {"id": ID}
    """No sacar de aqui no corre"""

    try:
        semantic_ = requests.get(DOMAIN_HOST, params = params)
        
        if "{" not in semantic_.text:
            print(semantic_.text)
            exit(0)

        response_  = loads(semantic_.text)

    except Exception as err:
        print(f"[ERROR] {err}")
        exit(0)

    denegado = response_["denegado"]
    permitido = response_["permitido"]

    # Se envian los datos para verificar la semantica del archivo
    check_ = check_semantic(permitido, denegado)

    if not check_:
        print(":: cerTI-cli :: Tu codigo no esta poniendo en practica lo aprendido ::")
        return False

    print(":: cerTI-cli :: Tu codigo si esta poniendo en practica lo que se esta evaluando ::")
    return True

def solve_():

    try:

        # Si es que se esta usando como archivo externo
        if TERMINAL:
            with open(RESP_SOLVE, "r") as read_:
                hash = read_.read().strip()

        # Si es que se esta importando como libreria
        else:
            hash = md5(RESP_SOLVE.encode("UTF-8")).hexdigest()

        data = {"key": ID, "solve": hash}

        response_ = requests.post(DOMAIN_HOST, data=data)
        print(response_.text)

    except Exception as err:
        print(f"[ERROR] {err}")
        return False

def resolve_tecnical(*args):
    """Funcion encargada de validar desde el propio codigo su validez"""
    global RESP_SOLVE
    
    RESP_SOLVE = str(args)

    if not ID:
        print(":: cerTI-cli :: No has declarado tu ID prueba con certi.ID = '<TU_ID>' ::")
        return
    
    if not FILE_CODE:
        print(":: cerTI-cli :: No has declarado la direccion a tu codigo prueba con certi.FILE_CODE = './tu/archivo.py' ::")
        return

    if len(ID) > 40 or len(ID) < 32:
        print(":: cerTI-cli :: Tu ID no cumple con el formato establecido ::")
        return
    
    solve_() if valid_() else exit(0)

if __name__ == "__main__":
    
    TERMINAL = True

    if len(argv) != 6 or all(x != argv[1] for x in params_) or "-R" not in argv or "-ID" not in argv:
        print(usage_); exit(0)

    RESP_SOLVE = argv[4]

    ID = argv[5]

    if argv[1] == "--check":
        valid_()

    elif argv[1] == "--solve":
        solve_() if valid_() else exit(0)

    else:
        print(usage_)