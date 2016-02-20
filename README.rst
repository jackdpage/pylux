Pylux
=====

.. image:: https://img.shields.io/pypi/v/pylux.svg
.. image:: https://img.shields.io/pypi/format/pylux.svg
.. image:: https://readthedocs.org/projects/pylux/badge/?version=latest

Pylux is a program for creating and managing documentation for stage lighting. 
The program uses an XML 'plot' file to store information about a lighting 
project. 

Pylux currently has the capability to, using the aforementioned plot files, 
generate plaintext documentation using Jinja2 (e.g. LaTeX or HTML documents), 
generate scale plan views of the lighting arrangement and, by calling 
mplayer, play sound cues.

Installation and Dependencies
-----------------------------

Pylux is in the early stages of development. It is not stable enough for 
general use.

Regular users should install Pylux from the PyPI using pip::

    sudo pip3 install pylux

In order to do this you will need the Python 3.5 interpreter::

    sudo apt install python3.5
    sudo pacman -S python

If you would rather use the most recent code, you can install from the Git 
repository::

    git clone https://github.com/jackdpage/pylux.git
    cd pylux
    sudo python3 setup.py install

Dependencies will be downloaded from the PyPI on installation. You will also 
need to manually install mplayer to play sound cues::

    sudo apt install mplayer
    sudo pacman -S mplayer

Documentation
-------------

The documentation for both users and contributers is available on 
`Read the Docs`_.

.. _`Read the Docs`: http://pylux.readthedocs.org/


Contributing
------------

Before making a contribution, please refer to the guidelines in 
``CONTRIBUTING.md``. If you are interested in contributing, there are many 
ways in which you can help:

+ [Python] writing code;
+ [XML] making fixture templates;
+ [SVG] making fixture symbols;
+ [Jinja] making ``reporter`` templates;
+ [English] submitting bug reports and feature requests.

License
-------

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
