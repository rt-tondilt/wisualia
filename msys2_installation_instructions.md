# How to install Wisualia on windows with MSYS2?

**Warning: This is a quite complex procedure. It may take several hours to
install everything correctly on an empty MSYS2 system depending on network and
computer speed. Also these instructions may not work, because they were tested
only once.**

## Installing MSYS2.

Goto [MSYS2 homepage](http://www.msys2.org) and install MSYS2. Both 32- and
64-bit installers should work. (See also [MSYS2 wiki](https://github.com/msys2/msys2/wiki)).

Now we have to update MSYS2.

Run **msys2 shell (`msys2\msys2.exe`)** and update package database.
`pacman -Syy`

Now do a full system upgrade. Run `pacman -Syuu` and follow the instructions.
Repeat untill everithing is up to date.

**NB**: MSYS2 can be used to install and compile both 64- and 32-bit programs. The
following guide assumes that you use **32-bit mingw shell
(`msys2\mingw32.exe`)** to install 32-bit Wisualia.

## General dependecies.

Install GTK 3, Python 3 and pip.

`pacman -S mingw-w64-i686-gtk3 mingw-w64-i686-python3-gobject mingw-w64-i686-python3-pip`

Also GtkSourceView.

`pacman -S mingw-w64-i686-gtksourceview3`

## moviepy and numpy

Pip has trouble installing numpy and pillow on MSYS2. So we have to install
these from the MSYS2 repo.

```
pacman -S mingw-w64-i686-python3-numpy
pacman -S mingw-w64-i686-python3-pillow
```

After that we can install moviepy.

`pip3 install moviepy`

## mypy

It turns out that we need gcc for installing mypy.

`pacman -S mingw32/mingw-w64-i686-gcc`

Also mypy has a dependency called psutil. We have to use the pacman version
because pip refuses to install it.

`pacman -S mingw-w64-i686-python3-psutil`

By the way, the pacman psutil version is too old for mypy. But because
mypy does not seem to use psutil very often, we can hope that this somehow works.

`pip3 install typed-ast`

`pip3 install mypy`

The last command should fail because pip can't install right psutil version.
However the last command installed all other dependencies. So now we can just
install mypy without dependencies.

`pip3 install mypy --no deps`

And check that there is only one conflict (the one with psutil).

```
$ pip3 check
mypy 0.560 has requirement psutil<5.5.0,>=5.4.0, but you have psutil 5.2.2.
```

## Other pip packages.

Pyglet and typing_extensions are neccessary.

```
pip3 install typing_extensions
pip3 install pyglet
```

You will only need the next two if you want to generate Wisualia documentation.
The editor and the library can run without them.

```
pip3 install sphinx
pip3 install sphinx-autodoc-typehints
```

## Installing AVbin

Pyglet needs AVbin to play mp3 files. Go to
[AVbin homepage](http://avbin.github.io/AVbin/Download.html) and download the
installer (`AVbin10-win32.exe`). Then run the installer and view installation
details.

Example installation details on my computer.

```
Create folder: C:\Program Files\AVbin
Extract: C:\Windows\system32\avbin.dll
Created uninstaller: C:\Program Files\AVbin\AVbin10-win32-uninstaller.exe
Create folder: C:\Users\Kasutaja\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\AVbin
Create shortcut: C:\Users\Kasutaja\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\AVbin\Uninstall AVbin.lnk
Completed
```

Note that the only thing we really need is `avbin.dll`.
We can copy `C:\Windows\system32\avbin.dll` to `msys2\mingw32\bin\avbin.dll`
and delete everything else.

## Installing Wisualia

Download wisualia from github and copy it to your user folder
(`msys2\home\Kasutaja`).

## Runnning Wisualia

```
Kasutaja@Muumid MINGW32 ~
$ cd wisualia/editor

Kasutaja@Muumid MINGW32 ~/wisualia/editor
$ python3 main.py
```

## Installing FFMPEG

Moviepy uses a package named imageio for some things.

Imageio needs a program named FFMPEG.

The developers of imageio thought that imageio should be easy to use. So the
first time imageio needs FFMPEG it downloads FFMPEG automatically to the AppData
directory. If we want to make portable (USB drive) version of Wisualia, then
we don't want to pollute the AppData directory of random computers. To avoid
this we have to do 2 things.

1. Export a random video with Wisualia to ensure that FFMPEG is installed.
2. copy
`C:\Users\Kasutaja\AppData\Local\imageio\ffmpeg\ffmpeg.win32.exe` to
`msys2\mingw32\bin\ffmpeg.exe`.

After that you may delete the `C:\Users\Kasutaja\AppData\Local\imageio` folder.

## Creating windows bundle

This step is fully automated. Go to the msys2 root folder and run
`home\Kasutaja\wisualia\create_windows_bundle.py`. Follow the instructions.
After finishing you should find a portable wisualia folder in MSYS2 root
directory.
