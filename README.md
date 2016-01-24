Pylux
=====

[![PyPI](https://img.shields.io/pypi/v/pylux.svg)](https://pypi.python.org/pypi/pylux/)
[![PyPI](https://img.shields.io/pypi/format/pylux.svg)](https://pypi.python.org/pypi/pylux#license)
[![Documentation Status](https://readthedocs.org/projects/pylux/badge/?version=latest)](http://pylux.readthedocs.org/en/latest/?badge=latest)

Pylux is a program for the management of lighting documentation written 
in Python. It uses its XML files called plots to store information about a 
lighting project.

The Pylux program comes with multiple 'contexts'. Each context has a specific 
command and feature set. Currently included are ``editor`` which allows for the 
editing of the aforementioned XML plots, ``reporter`` which creates reports 
from Jinja2 templates and ``plotter`` which creates SVG diagrams of the plot.

Installation and Dependencies
-----------------------------

Pylux is written in Python 3; you will need the Python 3 interpreter to run it.
You can either download a source distribution, then install by running 
```
sudo python setup.py install
```
or you can install directly from the PyPI using pip: 
```
pip install pylux
```

To install either way you will need Python, setuptools and pip, which are 
available from http://python.org or you can install them using your package 
manager:
```
sudo apt install python3 python3-pip python3-setuptools
```
```
sudo pacman -S python python-pip python-setuptools
```

Contributing
------------

If you are interested in contributing towards this project, there are many ways 
in which you can help:

+ [Python] writing code;
+ [XML] making fixture templates;
+ [SVG] making fixture symbols;
+ [Jinja] making ``reporter`` templates;
+ [English] submitting bug reports and feature requests.

License
-------

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
