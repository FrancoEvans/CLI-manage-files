from pathlib import Path

print(Path.cwd())
p = Path('automation/data/inbound/DATA2025.csv')

print(p.resolve())
if p.is_file():
    print('es un archivo')
else:
    print('no es un archivo')

data_path = Path('automation/data')

print(data_path in p.parents)
    