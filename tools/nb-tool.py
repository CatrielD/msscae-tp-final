#!/usr/bin/env python3

# para usar con:
# git difftool -x 'python git-nb-difftool.py' <commit> -- <path>
# o configurando en git
# - obtiene los contenidos y hace un diff ignorando la metadata
# - agrega banners para identificar las celdas
# - TODO
#   - más argumentos para configurar el tipo de banner de celdas
#   - poder hacer un diff por celda para tener line numbers de celdas
#   - como usar esto desde magit (emacs)?
# lo bueno de llamarlo desde difftool es que git se encarga del heavylifting de parsear commits y etc
# te da el archivo temporal de la versión especificada en el primer argumento

import os
import sys

from nbformat import read, NO_CONVERT
import subprocess
import tempfile

def cmd(*args) -> tuple:
    res = subprocess.run(args, shell=False, check=False, capture_output=True, text=True)
    return (res.stdout, res.returncode)


def nb_contents_as_str(
        nb_cells: dict,
        cell_banner = lambda n: f"\n\n######## Cell {n:02} ########\n\n") -> str:
    res = ''
    for no_cell, cell in enumerate(nb_cells["cells"]):
        res += cell_banner(no_cell)
        res += cell['source']
    return res

class NotebookContentReader:
    def __init__(self, path):
        self.path = path

    def err_msg(self):
        return f"ocurrió un error al intentar abrir el python notebook:\n\t{self.path}"

    def get_tmp_file(self, throw_on_error = True):
        if not self.path.endswith('.ipynb'):
            return open(self.path, 'r+t')
        f = tempfile.NamedTemporaryFile('w+t')
        try:
            f.write(nb_contents_as_str(read(self.path, NO_CONVERT)))
            f.seek(0)
            return f
        except Exception as e:
            msg = self.err_msg()
            print(f"{msg}\nabortando...")
            if throw_on_error:
                raise e
            sys.exit(5)


if __name__ == "__main__":
    import argparse
    import pathlib
    parser = argparse.ArgumentParser()
    parser.add_argument('--diff-tool', nargs=2,
                        help="para usarlo de difftool en git, hace un diff entre <path-to-tmp-file-local> <path-to-tmp-file-revisión>",
                        type=pathlib.Path)
    parser.add_argument('--show', help='mostrar el contenido de las celdas, sin los resultados, por ahora solo <path-to-tmp-file-local> sin revisiones', type=pathlib.Path)
    parser.add_argument('--banner', help="TODO: cambiar el banner de cada celda")
    args = parser.parse_args()
    #print(args)
    #sys.exit(-1)
    if args.diff_tool:
        # also know as LOCAL REMOTE ... for reasons
        [REVISION_PATH, WORKING_PATH] = sys.argv[2:]
        with NotebookContentReader(REVISION_PATH).get_tmp_file() as revision:
            with NotebookContentReader(WORKING_PATH).get_tmp_file() as working:
                out, err = cmd('diff', revision.name, working.name)
                if err == 1:
                    print(out)
                sys.exit(err)
    if args.show:
        maybe_file = sys.argv[2]
        if maybe_file == "-":
            with tempfile.NamedTemporaryFile("w+t") as temp:
                temp.writelines(sys.stdin.readlines())
                temp.seek(0)
                print(nb_contents_as_str(read(temp.name, NO_CONVERT)))
        else:
            print(nb_contents_as_str(read(maybe_file, NO_CONVERT)))

