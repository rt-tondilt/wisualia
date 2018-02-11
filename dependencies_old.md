ddddddddMSYS_setup_2.md
MSYS2 kasutamine
============================
* Goto http://www.msys2.org
* Download "msys2-x86_64-20161025.exe"
* Run installer
* Select installation folder "C:/Programs/msys64"
* Close installer
* Delete installer

* MSYS2 should require about 228 MB

* Read https://github.com/msys2/msys2/wiki

NB: MSYS2 has 3 shells:
* mingw32.exe for building native Windows 32 bit applications
* mingw64.exe for building native Windows 64 bit applications
* msys2.exe for running posix applications

* We want to have maximal portability so we use mingw32.exe.

* Read about pacman usage: https://github.com/msys2/msys2/wiki/Using-packages.

* Update package database `pacman -Syy`. Very neccessary.

* run `pacman -S mingw-w64-i686-gtk3 mingw-w64-i686-python3-gobject`, doing that
we also install:
`mingw-w64-i686-python3-3.6.2rc1-2
mingw-w64-i686-python3-cairo-1.13.3-2
mingw-w64-i686-python3-gobject-3.24.1-2`
* It took about 4 minutes on my computer.
* Check python version, should be 3.6
```
$ python3
Python 3.6.2rc1 (default, Jun 26 2017, 07:51:29)  [GCC 6.3.0 32 bit] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
* Try example from  https://pygobject.readthedocs.io/en/latest/getting_started.html,
  use python3.

`pacman -S mingw-w64-i686-python3-pip`
`pip3 install moviepy`
`pacman -S mingw-w64-i686-toolchain` it installed python 2 damn.
`pip3 install moviepy`
`pip3 install mypy`

`pacman -S mingw-w64-i686-gtksourceview3`
`pacman -S mingw-w64-i686-glade`


```text
It worked. Now install styrene.
`pacman -S --needed zip \
  mingw-w64-x86_64-python3 \
  mingw-w64-x86_64-gcc mingw-w64-x86_64-nsis mingw-w64-x86_64-binutils \
  mingw-w64-i686-python3 \
  mingw-w64-i686-gcc mingw-w64-i686-nsis mingw-w64-i686-binutils`
`pacman -S --needed git` probably unnecesary

`git clone https://github.com/achadwick/styrene.git
cd styrene
pip3 install .`
```
