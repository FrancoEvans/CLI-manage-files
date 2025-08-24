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
    "pobreza-datos.csv"
]

for filename in filenames:
    file = inbound / filename
    file.touch(exist_ok=True)