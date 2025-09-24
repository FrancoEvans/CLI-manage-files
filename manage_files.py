from pathlib import Path
import argparse
from datetime import datetime
import pandas as pd

def build_parser():
    p = argparse.ArgumentParser(
        prog= "manage_files",
        description= ''
    )

    # ARGUMENTOS GLOBALES
    p.add_argument('--src', type=Path, required=True) 
    p.add_argument('--pattern', type=str, default='*', help='ej: "*.csv"') 
    p.add_argument('--dry-run', action="store_true")
    p.add_argument('--log-file', type=Path)

    # SUB PARSERS
    sub = p.add_subparsers(dest='cmd', required=True)

    # SUB PARSER RENAME
    sp = sub.add_parser("rename")
    sp.add_argument("--rule", required=True, help='ej: {stem}_2025{suffix}')

    # SUB PARSER MOVE
    sp = sub.add_parser("move")
    sp.add_argument("--by", choices=["mtime","ctime"], default="mtime")
    sp.add_argument("--dest", type=Path, required=True)

    # SUB PARSER MERGE
    sp = sub.add_parser("merge")
    sp.add_argument("--out", type=Path, required=True)

    # SUB PARSER LS
    sp = sub.add_parser('ls')

    return p



def normalize_name(name):
    translates = str.maketrans(' -áéíóúÁÉÍÓÚ', '__aeiouaeiou')
    return Path(name.lower().translate(translates))

def unique_name(dst_dir: Path, filename: str):
    p = Path(filename)
    stem, suffix = p.stem, p.suffix

    path = dst_dir / filename
    if not path.exists():
        return filename
    
    i = 1
    while True:
        new_filename = f'{stem}-{i}{suffix}'
        path = dst_dir / new_filename
        if not path.exists():
            return new_filename
        else:
            i+=1
        
def cmd_rename(args):
    for f in args.src.glob(args.pattern):
        if f.is_file():
            n = normalize_name(f.name)
            new_name = args.rule.format(
                name = n.name, stem = n.stem, suffix = n.suffix
            )
            new = f.with_name(unique_name(args.src, new_name))
            f.rename(new)

def cmd_move(args):
    # obtener fecha + crear carpeta destino + mover archivo.
    src_path = args.src.resolve()
    dst_dir = args.dest.resolve()

    errores = 0
    movidos = 0
    saltados = 0

    if dst_dir.is_relative_to(src_path):
        raise ValueError("dst no puede estar dentro de src")
        
    for f in sorted(src_path.glob(args.pattern)):
        if f.is_file():
            try:
                st = f.stat()
                match args.by:
                    case 'mtime':
                        dt = datetime.fromtimestamp(st.st_mtime)
                    case 'ctime':
                        dt = datetime.fromtimestamp(st.st_ctime)
                    case _:
                        dt = datetime.fromtimestamp(st.st_mtime)
                subdir = dt.strftime("%Y-%m")
                final_dir = dst_dir / subdir
                final_dir.mkdir(parents=True, exist_ok=True)
                filename = unique_name(final_dir, f.name)
                dst_path = final_dir / filename
                if not f.resolve() == dst_path.resolve():
                    f.rename(dst_path)
                    movidos += 1
                else:
                    saltados += 1
        
            except Exception as e:
                print(f'error: {str(e)}')
                errores += 1
        else:
            saltados += 1
    print(f'movidos={movidos}, saltados={saltados} errores={errores}')



    

def cmd_merge(args):
    # abrir CSVs + concatenar + agregar columna + guardar master.
    src_path = args.src.resolve()
    out_dir = args.out.resolve()
    date = datetime.now()
    master_csv = out_dir / f'master_{date.strftime("%Y-%m-%d")}.csv'

    dataframes = []

    if not src_path.exists():
        print(f'no se encontro la ruta: {src_path}')
        return

    for i, f in enumerate(sorted(src_path.glob(args.pattern))):
        if f.suffix == '.csv':
            df = pd.read_csv(f)

            df['_source_file'] = f.name
            df['_at'] = date.strftime("%Y-%m-%dT%H:%M")
            
            dataframes.append(df)

            print(f'archivo {i+1} ready > {f.name}')

    if not dataframes:
        print("no se encontraron csv's")
        return
    
    master_df = pd.concat(dataframes)

    # columnas tecnicas al final
    columns = master_df.columns
    no_native_columns = ['_source_file', '_at']
    native_columns = [c for c in columns if c not in no_native_columns]
    
    master_df = master_df[native_columns + no_native_columns]

    print(f'concatenados los {len(dataframes)} archivos')

    master_df.to_csv(master_csv, index=False)

    print(f'{master_csv.name} guardado en {master_csv.parent}')

# ejecutable
# python automation/manage_files.py --src automation/data/test_data  --pattern "*.csv" merge --out automation/out_dst_prueba


def cmd_ls(args):
    for f in args.src.iterdir():
        print(f.name)

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "rename":
        cmd_rename(args)
    elif args.cmd == "move":
        cmd_move(args)
    elif args.cmd == "merge":
        cmd_merge(args)
    elif args.cmd == 'ls':
        cmd_ls(args)

if __name__ == '__main__':
    main()