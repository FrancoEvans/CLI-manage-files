from pathlib import Path

import pandas as pd

folder = Path(__file__).resolve().parent

df1 = pd.DataFrame({
    "id": range(1, 6),
    "nombre": ["Ana", "Luis", "María", "Pedro", "Lucía"],
    "edad": [23, 30, 27, 35, 29]
})

df2 = pd.DataFrame({
    "producto": ["Arroz", "Fideos", "Leche", "Pan", "Queso", "Tomate"],
    "precio": [120, 90, 150, 80, 200, 75],
    "stock": [30, 50, 20, 40, 15, 60]
})

df3 = pd.DataFrame({
    "materia": ["Álgebra", "Programación", "Arquitectura", "TGS", "Discreta"],
    "nota": [7, 9, 6, 8, 10],
    "aprobado": [True, True, True, True, True]
})

# Guardar como CSVs
path1 = folder / 'personas.csv'
path2 = folder / 'productos.csv'
path3 = folder / 'notas.csv'

df1.to_csv(path1, index=False)
df2.to_csv(path2, index=False)
df3.to_csv(path3, index=False)

path1, path2, path3

