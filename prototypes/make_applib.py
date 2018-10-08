import os
from pathlib import Path
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

if __name__ == '__main__':
    import sys
    z = None
    if len(sys.argv) > 2:
        lib = sys.argv[2]
        z = ZipFile(lib, "w")
    src = Path(sys.argv[1])
    for p in walker(src, prune=prune):
        print(p)
        if z: z.write(src/p, arcname=p)

    if z:
        z.close()
        make_zapps(src, lib)
