import requests
import os

dirs_ = os.listdir(".")

if "certi.py" not in dirs_:
    print(":: cerTI-Installer :: Error, no estas ejecutando cerTI desde la carpeta de prueba tecnica ::")
    exit(0)

try:
    print(":: cerTI-Installer :: Descargando la version actualizada de cerTI-CLI ::")
    certi_get = requests.get("https://raw.githubusercontent.com/ciberuniverse/server_status/refs/heads/main/certi_cli/certi.py", timeout=20)
    certi_file = certi_get.text

except Exception as err:
    print(":: cerTI-Installer :: Error, no se logro obtener la version actualizada de cerTI-CLI ::")
    exit(0)

os.remove("certi.py")
with open("certi.py", "w", encoding="utf-8") as save_:
    save_.write(certi_file)
print(":: cerTI-Installer :: cerTI-CLI se actualizo correctamente, corre python3 certi.py --gui para usar la GUI ::")