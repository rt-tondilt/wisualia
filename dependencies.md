``pacman -Syy
pacman -Syuu
pacman -Syuu
pacman -Syuu
pacman -S mingw-w64-i686-gtk3 mingw-w64-i686-python3-gobject mingw-w64-i686-python3-pip
pacman -S mingw-w64-i686-python3-numpy
pacman -S mingw-w64-i686-python3-pillow
pip3 install moviepy
pacman -S mingw-w64-i686-python3-psutil
pacman -S mingw32/mingw-w64-i686-gcc
pip3 install typed-ast
pip3 install mypy
pip3 install mypy --no deps
``
``$ pip3 check
mypy 0.560 has requirement psutil<5.5.0,>=5.4.0, but you have psutil 5.2.2.
``

``pip3 install typing_extensions
pip3 install pyglet
pip3 install sphinx
pip3 install sphinx-autodoc-typehints
pacman -S mingw-w64-i686-gtksourceview3
``
Install avbin from internet
``http://avbin.github.io/AVbin/Download.html``
``AVbin10-win32.exe``
Run it.
``Create folder: C:\Program Files\AVbin
Extract: C:\Windows\system32\avbin.dll
Created uninstaller: C:\Program Files\AVbin\AVbin10-win32-uninstaller.exe
Create folder: C:\Users\Kasutaja\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\AVbin
Create shortcut: C:\Users\Kasutaja\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\AVbin\Uninstall AVbin.lnk
Completed
``
We don't like it so we copy ``C:\Windows\system32\avbin.dll`` to
the ``msys2\mingw32\bin\avbin.dll`` folder.

Now run wisualia:
``Kasutaja@Muumid MINGW32 ~
$ cd wisualia/editor

Kasutaja@Muumid MINGW32 ~/wisualia/editor
$ python3 main.py``
and export a video.

This should run moviepy which imports imageio which installs ffmpeg to:
``C:\Users\Kasutaja\AppData\Local\imageio\ffmpeg\ffmpeg.win32.exe``.
copy this to ``msys2\mingw32\bin\ffmpeg.exe``

Now make windows bundle.
