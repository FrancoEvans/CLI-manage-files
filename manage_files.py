from pathlib import Path
import argparse

def build_parser():
    p = argparse.ArgumentParser(
        prog= "manage_files",
        description= ''
    )

    # ARGUMENTOS GLOBALES
    p.add_argument('--src', type=Path, required=True)
    p.add_argument('--pattern', type=str, default='*')
    p.add_argument('--dry-run', action="store_true")
    p.add_argument('--log-file', type=Path)

    # SUB PARSERS
    sub = p.add_subparsers(dest='cmd', required='True')

    # SUB PARSER RENAME
    sp = sub.add_parser("rename")
    sp.add_argument("--rule", required=True)

    # SUB PARSER MOVE
    sp = sub.add_parser("move")
    sp.add_argument("--by", choices=["mtime","ctime"], default="mtime")
    sp.add_argument("--dest", type=Path, required=True)

    # SUB PARSER MERGE
    sp = sub.add_parser("merge")
    sp.add_argument("--out", type=Path, required=True)

def cmd_rename():
    # encontrar archivos + normalizar nombres + renombrar.
    ...

def cmd_move():
    # obtener fecha + crear carpeta destino + mover archivo.
    ...

def cmd_merge():
    # abrir CSVs + concatenar + agregar columna + guardar master.
    ...

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.cmd == "rename":
        ...
    elif args.cmd == "move":
        ...
    elif args.cmd == "merge":
        ...