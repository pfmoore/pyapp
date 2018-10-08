import subprocess
import sys
import tempfile
import zipapp

import click
from pkg_resources import WorkingSet, Requirement

# TODO: `--command xxx` uses entry point xxx for the main routine and
#       output file name

@click.command()
@click.option('--main', default=None)
@click.option('--output', default=None)
@click.argument('req', nargs=-1)
def make_zipapp(main, output, req):
    with tempfile.TemporaryDirectory() as target:
        subprocess.call([
            sys.executable, '-m', 'pip',
            'install',
            '--target', target,
            ] + list(req))

        if main is None:
            ws = WorkingSet([target])
            r = Requirement.parse(req[0])
            for ep in ws.iter_entry_points(group='console_scripts'):
                if ep.dist in r:
                    main = ep.module_name + ':' + ('.'.join(ep.attrs))
                    if output is None:
                        output = ep.name + '.pyz'
                    break
        zipapp.create_archive(target, output, main=main)

if __name__ == '__main__':
    make_zipapp()
