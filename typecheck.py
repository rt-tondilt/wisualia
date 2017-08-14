
import sys
import inspect
import subprocess
from editor.dir_tools import get_dir


result = subprocess.check_output(['mypy', get_dir('library/wisualia'), '--config-file', get_dir('library/wisualia/mypy.ini')],
                                 universal_newlines=True, shell=True)
if result != '':
    print(result)

print('Finished type checking.')
