import os
from pathlib import Path
from zipfile import ZipFile

def walker(dirname, prune=None):
    for dirpath, dirnames, filenames in os.walk(dirname):
        p = Path(dirpath).relative_to(dirname)
        if prune:
            dirnames[:] = [d for d in dirnames if not prune(d)]
        for f in filenames:
            yield p / f

def prune(d):
    if d == 'bin': return True
    if d.endswith('.dist-info'): return True
    if d == '__pycache__': return True
    return False

if __name__ == '__main__':
    import sys
    z = None
    if len(sys.argv) > 2:
        z = ZipFile(sys.argv[2], "w")
    src = Path(sys.argv[1])
    for p in walker(src, prune=prune):
        print(p)
        if z: z.write(src/p, arcname=p)
    if z: z.close()
