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
    sub = p.add_subparsers(dest='command', required=True)

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


# FUNCIONES

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

# 2025-09-24 21:14:52 [INFO] move: Movido ventas.csv -> archive/2025-09/ventas.csv
# 2025-09-24 21:14:52 [WARNING] rename: Nombre duplicado, creado ventas-1.csv
def log(args, flag_index: int, message: str):

    log_file = args.log_file
    dry_run = args.dry_run

    if log_file is None:
        return
    
    if not log_file.parent.exists():
        print(f'No existe la ruta {log_file} -> Creada')
        log_file.parent.mkdir(parents=True, exist_ok=True)

    # creacion del mensaje log
    flags = ['INFO', 'ERROR', 'WARNING']
    command = args.command
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_msg = f'{date} [{flags[flag_index]}] {command}: {message}' if not dry_run else f'{date} [{flags[flag_index]}] [DRY] {command}: {message}'

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{log_msg}\n")
    print(log_msg)


# COMANDOS 

def cmd_rename(args):
    for f in args.src.glob(args.pattern):
        if f.is_file():
            new_name = args.rule.format(
                name = f.name, stem = f.stem, suffix = f.suffix
            )
            new_name = normalize_name(new_name)
            new = f.with_name(unique_name(args.src, new_name))
            if not args.dry_run:
                f.rename(new)
            log(args, 0, f'Archivo renombrado {f.name} -> {new_name}')

# ejecutable
# python automation/manage_files.py --src automation/data/test_data  --pattern "ventas.csv" --log-file automation/log/register.log rename --rule '{stem}_2025{suffix}'

def cmd_move(args):
    # obtener fecha + crear carpeta destino + mover archivo.
    src_path = args.src.resolve()
    dst_dir = args.dest.resolve()

    errores = 0
    movidos = 0
    saltados = 0

    if dst_dir.is_relative_to(src_path):
        log(args, 1, "La carpeta destino no puede estar dentro de source")
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

                if filename != f.name:
                        log(args, 2, f'Nombre duplicado ({f.name}), creado {filename}')

                if not f.resolve() == dst_path.resolve():
                    if not args.dry_run: 
                        f.rename(dst_path)
                    movidos += 1
                    log(args, 0, f'Movido {f.name} -> {dst_path}')

                else:
                    saltados += 1
                    log(args, 2, f'Archivo saltado {f.name}')
        
            except Exception as e:
                print(f'error: {str(e)}')
                errores += 1
                log(args, 1, f'Error moviendo {f.name}')
        else:
            saltados += 1
    print(f'movidos={movidos}, saltados={saltados} errores={errores}')

# ejecutable
# python automation/manage_files.py --src automation/data/inbound  --pattern "*.csv" move --rule '{stem}_2024{suffix}'

    
def cmd_merge(args):
    # abrir CSVs + concatenar + agregar columna + guardar master.
    src_path = args.src.resolve()
    out_dir = args.out.resolve()
    date = datetime.now()
    master_csv = out_dir / f'master_{date.strftime("%Y-%m-%d")}.csv'

    if master_csv.exists():
        backup = master_csv.with_suffix(master_csv.suffix + ".bak")
        if not args.dry_run:
            master_csv.rename(backup)
        log(args, 2, f'Master ya existía, movido a {backup.name}')

    dataframes = []

    if not src_path.exists():
        print(f'no se encontro la ruta: {src_path}')
        log(args, 1, f'No se encontro la ruta {src_path}')
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
    
    if not args.dry_run:
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

    if args.command == "rename":
        cmd_rename(args)
    elif args.command == "move":
        cmd_move(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == 'ls':
        cmd_ls(args)

if __name__ == '__main__':
    main()