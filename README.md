# Pylux

Pylux is a program for the management of lighting documentation written 
in Python. It uses its XML files called plots to store information about a 
lighting project.

Currently Pylux consists of a program for editing these plot files, 
``editor``, a couple of extensions and some bundled lighting fixture data.

The ``plotter`` extension produces lighting plot diagrams in SVG format 
and the ``texlux`` extension produces documentation based on Jinja 
templates. This is intended for but not limited to LaTeX documentation.

Pylux is currently only functional on the CLI. A GUI is planned but is not 
a priority.

## Installation and Dependencies

Pylux is written in Python 3, so the Python 3 interpreter is required. You 
will also need pip and setuptools. These are all available from  
http://python.org, or you can install them using your package manager:

`sudo apt install python3 python3-pip python3-setuptools`

`sudo pacman -S python python-pip python-setuptools`

Once you have installed the basic Python dependencies, download the latest 
version of Pylux and to install, run ``sudo python setup.py install``.

This will download any additional dependencies from the PyPI.

To use Pylux, simply run ``pylux`` in a shell.

## Contributing
If you are interested in contributing towards this project, there are many ways 
in which you can help:

+ [Python] writing code;
+ [XML] making fixture templates;
+ [SVG] making fixture symbols;
+ [LaTeX/Jinja] making ``texlux`` templates;
+ [English] submitting bug reports and feature requests.

## License

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
