
import sys
import inspect
from subprocess import run, PIPE,STDOUT
from editor.dir_tools import relative_to_wisualia


result = run(['mypy', relative_to_wisualia('library/wisualia'), '--config-file',
    relative_to_wisualia('library/wisualia/mypy.ini')],
    universal_newlines=True, shell=True,stdout=PIPE,stderr=STDOUT).stdout

if result != '':
    print(result)

print('Finished type checking.')
