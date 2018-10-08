import argparse
import os
from pathlib import Path
import shutil
from zipfile import ZipFile

from pkg_resources import WorkingSet, Requirement

def walker(dirname, prune=None):
    for dirpath, dirnames, filenames in os.walk(dirname):
        p = Path(dirpath).relative_to(dirname)
        if prune:
            dirnames[:] = [d for d in dirnames if not prune(d)]
        for f in filenames:
            yield p / f

def mainfile(ep, lib):
    module = ep.module_name
    fn = '.'.join(ep.attrs)
    lib = str(lib)

    MAIN = f"""\
# -*- coding: utf-8 -*-
import sys
import os
pyz_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(pyz_dir,{lib!r}))
import {module}
{module}.{fn}()
"""

    return MAIN

def make_zapps(dirname, lib):
    ws = WorkingSet([dirname])
    for ep in ws.iter_entry_points(group='console_scripts'):
        main = ep.module_name + ':' + ('.'.join(ep.attrs))
        output = ep.name + '.pyz'
        with ZipFile(output, 'w') as z:
            z.writestr('__main__.py', mainfile(ep, lib))

def prune(d):
    if d == 'bin': return True
    if d.endswith('.dist-info'): return True
    if d == '__pycache__': return True
    return False

def makelib_dir(src, dst):
    def ignore(dirname, files):
        return [f for f in files if prune(f)]
    shutil.copytree(src, dst, ignore=ignore)

def makelib_zip(src, dst):
    src = Path(src)
    with ZipFile(dst, "w") as z:
        for p in walker(src, prune=prune):
            z.write(src/p, arcname=p)

def main(args=None):
    """Run the make_applib command line interface.

    The ARGS parameter lets you specify the argument list directly.
    Omitting ARGS (or setting it to None) works as for argparse, using
    sys.argv[1:] as the argument list.
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--compress', '-c', default=True, action='store_true',
            help="Create a zipped library file")
    parser.add_argument('--no-compress', action='store_false', dest='compress',
            help=argparse.SUPPRESS)
    parser.add_argument('--lib', '-L', default=None,
            help="The name of the library file to create.")
    parser.add_argument('prep', default=None,
            help="The name of the prepared distribution directory.")

    args = parser.parse_args(args)

    if args.lib is None:
        if args.compress:
            args.lib = args.prep + '.zip'
        else:
            args.lib = args.prep + '_lib'

    print(f"args.prep={args.prep}, args.lib={args.lib}, args.compress={args.compress}")

    if args.compress:
        makelib_zip(args.prep, args.lib)
    else:
        makelib_dir(args.prep, args.lib)

    make_zapps(args.prep, args.lib)

if __name__ == '__main__':
    main()
