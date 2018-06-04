# How to install Wisualia on GNU/Linux?

*These instructions have only been tested on Ubuntu 18.04.*

Firstly we need python 3.6 and pip.
```
sudo apt install python3 python3-pip
```

Now other dependencies from APT.
```
sudo apt install python3-gi python3-gi-cairo libgtksourceview-3.0-1
```

And pip packages.
```
pip3 install moviepy mypy typing_extensions
```

You will need the next two if you want to generate Wisualia documentation.
The editor and the library can run without them.

```
pip3 install sphinx sphinx-autodoc-typehints
```

The last step is downloading the Wisualia repository from Github.
