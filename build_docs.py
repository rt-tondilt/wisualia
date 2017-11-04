import os
import shutil
import sys
import subprocess

help_text='''
Wisualia documentation generation script
========================================

This script generates Wisualia documentation. You can run this script with any
Python interpreter: native CPython or the one that comes with Wisualia.

Arguments:

    <none>        Generate documentation, do not delete old files.

    -h, --help    Show this help text.

    --clean       Delete all built documentation files in _apidoc and _build
                  directories and regenerate all files. This option
                  is neccessary if you have deleted or renamed files and
                  might also be neccessary if you have changed .rst files.
'''

import __main__
os.chdir(os.path.dirname(os.path.abspath(__main__.__file__)))

wisualia_dir = os.path.dirname(os.getcwd())
python = os.path.join(wisualia_dir, 'mingw32/bin/python3.6.exe')


def run(name, task):
    print()
    print('=======================')
    print('    RUNNING', name)
    print('=======================')
    completed_process = subprocess.run(task)


if len(sys.argv)==2:
    if sys.argv[1] in ['-h', '--help']:
        print(help_text)
        exit()
    elif sys.argv[1] == '--clean':
        for place in ['docs/_apidoc', 'docs/_build', 'docs/_images']:
            try:
                shutil.rmtree(place)
            except FileNotFoundError:
                pass
    else:
        print('ERROR: Unknown argument')
        print(help_text)
        exit()
elif len(sys.argv)>2:
    print('ERROR: To many arguments.')
    print(help_text)
    exit()


print('           BUILDING DOCS')
print('====================================')

if not os.path.exists('docs/_images'):
    os.makedirs('docs/_images')

run('APIDOC', [python, '-m', 'sphinx.apidoc', '-feT', 'library/wisualia', '-o', 'docs/_apidoc'])
run('DOCTEST', [python, '-m', 'sphinx', '-b', 'doctest', 'docs', 'docs/_build'])
run('BUILD', [python, '-m', 'sphinx', 'docs', 'docs/_build'])
