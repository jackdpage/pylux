# Pylux

Pylux is a suite for the management of lighting documentation. It comes with 
a base program, ``plotter``, which is used to edit its plot XML files. From 
the base program, you can also call extensions which perform other functions.
Current extensions in development are ``texlux`` for producing LaTeX reports 
and ``plotgen`` for producing SVG plots.

``plotter`` currently is only functional on the CLI, but a GUI is in 
development.

## Installation and Dependencies

THIS PROGRAM IS NOT FUNCTIONAL ON WINDOWS. The program installs and searches 
for content in ``/usr/share/pylux``, so you will need a UNIX based computer. 
I will make it work on Windows when I can be bothered.

Pylux is written in Python 3, so the Python 3 interpreter is required.

To install, run ``sudo python setup.py install``.

Texlux does not require LaTeX to be installed to produce the reports, as they 
are produced as LaTeX source, however, you will need a LaTeX distribution, such 
as TeX Live, installed in order to build PDF files from this source.

## Contributing
If you are interested in contributing towards this project, there are many ways 
in which you can help:

### Writing code
If you know Python you can contribute by either adding to the base program and 
API or by writing your own extensions which can be implemented into the 
program. The manual (found in the ``docs`` folder) fully documents how to use 
the API to write your own extensions. Most of Pylux is documented using 
docstrings but the manual will be more up-to-date.

### Making new fixtures
If you know XML, you can write new fixture files, short XML files used by 
Pylux to create new fixtures based on an existing template. These are located 
in the ``fixture`` folder.

### Writing documentation
If you know LaTeX and understand how Pylux works, you can write documentation. 
There is currently a single manual for the whole of Pylux (including bundled 
extensions) in the ``docs`` folder.

### Creating fixture symbols
If you know SVG (or Inkscape if that's your thing), you can create new 
fixture symbols to implement into SVG plots (which are NYI). If you can find 
some free SVG symbols somewhere that would be even better.

### Submitting bugs and feature requests
If you know English, you can still help by submitting any bugs you come 
across to the GitHub issues tracker for this repository. Feel free to submit 
feature requests also (but not too many).

See ``TODO.txt`` to see what needs to be done.
Everything (including fixture files and symbols) should be edited on a fork 
and then a pull request submitted.

## License

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
