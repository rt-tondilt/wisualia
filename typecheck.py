
import sys
import inspect
from subprocess import run, PIPE,STDOUT
from editor.dir_tools import get_dir


result = run(['mypy', get_dir('library/wisualia'), '--config-file',
    get_dir('library/wisualia/mypy.ini')],
    universal_newlines=True, shell=True,stdout=PIPE,stderr=STDOUT).stdout

if result != '':
    print(result)

print('Finished type checking.')
