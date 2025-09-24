from pathlib import Path

inbound = Path("automation/data/inbound")
inbound.mkdir(parents=True, exist_ok=True)

filenames = [
    "Ventas 10.csv",
    "ventas_10.csv",
    "Analisis.csv",
    "analisis pobreza.csv",
    "Informe-Ventas.csv",
    "DATA2025.csv",
    "Resumen Final.csv",
    "ventas_MARZO.csv",
    "Reporte_Anual_2024.csv",
    "pobreza-datos.csv",
]

for filename in filenames:
    file = inbound / filename
    file.touch(exist_ok=True)

# df 1 (analisis pobreza.csv)

# provincia,region,pobreza_pct,anio
# Buenos Aires,Centro,32.5,2023
# Cordoba,Norte,28.4,2023
# Santa Fe,Centro,25.1,2023

# df 2 (pobreza-datos.csv)

# provincia,hogares_pobres,anio
# Buenos Aires,23000,2023
# Cordoba,12500,2023
# Mendoza,8900,2023
