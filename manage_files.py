from pathlib import Path
import argparse

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
    
    ...

def cmd_merge():
    # abrir CSVs + concatenar + agregar columna + guardar master.
    ...

def cmd_ls(args):
    for f in args.src.iterdir():
        print(f.name)

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "rename":
        cmd_rename(args)
    elif args.cmd == "move":
        ...
    elif args.cmd == "merge":
        ...
    elif args.cmd == 'ls':
        cmd_ls(args)

if __name__ == '__main__':
    main()