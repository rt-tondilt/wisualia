import os
import shutil
import glob

question = '''
Wisualia Windows bundle script
==========================

This script takes neccessary files from msys2 mingw32 system and
bundles them to minimal Windows distribution, that includes:
    * Wisualia
    * Python 3.6 and standard libray
    * Other necessary python libraries
    * Neccessary dll-s.
    * Icons
and does not include:
    * shells
    * glade
    * pip
    * C code and header files

NB: This script only works, if run inside msys2 root directory.
NB: It may take "some" minutes.

Do you want to make minimal windows bundle? [Y/N]'''
if input(question).upper() != 'Y':
    exit()

default = 'home/Rando/wisualia'
text = '''
Enter path of wisualia-python relative to msys2 root directory.
The default path is "{}"
Enter path:'''.format(default)
location = input(text)
if location == '':
    location = default

print('Running..')

os.makedirs('wisualia-msys2')

shutil.copytree(location, 'wisualia-msys2/wisualia')

os.makedirs('wisualia-msys2/mingw32')
os.makedirs('wisualia-msys2/mingw32/bin')


bin_files = [
    'mingw32/bin/python3.6.exe',
    'mingw32/bin/python3.6m.exe',
    'mingw32/bin/mypy.exe',
    'mingw32/bin/ffmpeg.exe',
    ]

for path in glob.iglob('mingw32/bin/*.dll'):
    bin_files.append(path)

for b in bin_files:
    shutil.copy(b, 'wisualia-msys2/'+b)


dirs = [
    'mingw32/etc',

    'mingw32/lib/gdk-pixbuf-2.0',
    'mingw32/lib/gio',
    'mingw32/lib/girepository-1.0',
    'mingw32/lib/glib-2.0',
    'mingw32/lib/gtk-3.0',
    'mingw32/lib/mypy',
    'mingw32/lib/python3.6',

    'mingw32/share/gir-1.0',
    'mingw32/share/glade',
    'mingw32/share/glib-2.0',
    'mingw32/share/gtk-3.0',
    'mingw32/share/gtk-doc',
    'mingw32/share/gtksourceview-3.0',
    'mingw32/share/icons',
    ]

for d in dirs:
    shutil.copytree(d, 'wisualia-msys2/'+d)

batch_script = r'''
REM A variable is needed, because python multiprocessing module wants absolute main file location.
SET wisualia-main-path=%~dp0wisualia\editor\main.py
mingw32\bin\python3.6.exe  %wisualia-main-path% ||  pause
'''

with open('wisualia-msys2/wisualia.cmd', 'w') as f:
    f.write(batch_script)

print('FINISHED')
