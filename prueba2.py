import pandas as pd
from pathlib import Path
from datetime import datetime

cwd = Path.cwd()
csv_folder = cwd / 'automation/data/inbound'
df1_src = cwd / csv_folder / 'analisis pobreza.csv'
df2_src = cwd / csv_folder / 'analisis pobreza.csv'
out_dst = cwd / 'automation/out_dst_prueba'


if df1_src.exists() and df2_src.exists():

    df1 = pd.read_csv(df1_src)
    df2 = pd.read_csv(df2_src)

    out_dst.mkdir(exist_ok=True)

    columns1 = set(df1.columns)
    columns2 = set(df2.columns)

    columns = columns1 | columns2


    

