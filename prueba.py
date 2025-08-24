from pathlib import Path

import shutil

p = Path('automation/prueba')

print(Path.cwd())
print(p.resolve())

p # path al directorio
p.mkdir(exist_ok=True) # la crea 
if not any(p.iterdir()):
    p.rmdir() # la borra (vacia)
else:
    shutil.rmtree(p) # la borra



p.mkdir()

file = p / 'archivo.csv'
file.touch()
if file.exists():
    print(file.resolve())

p2 = Path('automation/prueba_2')


p2.mkdir(exist_ok=True)

print(file.parent)
file.rename(p2 / file.name)
print(file.resolve())



import datetime


if file.exists():
    info = file.stat()   # objeto con metadata del archivo
    print("Tamaño:", info.st_size, "bytes")
    print("Creación:", datetime.datetime.fromtimestamp(info.st_ctime))
    print("Último acceso:", datetime.datetime.fromtimestamp(info.st_atime))
    print("Última modificación:", datetime.datetime.fromtimestamp(info.st_mtime))
