Pylux
=====

.. image:: https://img.shields.io/pypi/v/pylux.svg
.. image:: https://img.shields.io/pypi/format/pylux.svg
.. image:: https://readthedocs.org/projects/pylux/badge/?version=latest

Pylux is a program for creating and managing documentation for stage lighting. 
The program uses an XML 'effects plot' file to store information about a lighting 
project. 

Pylux currently has the capability to, using the aforementioned plot files, 
generate plaintext documentation using Jinja2 (e.g. LaTeX or HTML documents), 
generate scale plan views of the lighting arrangement and, by calling 
mplayer, play sound cues.

Installation and Dependencies
-----------------------------

Pylux is written in Python 3, so you will need the usual Python dependencies, 
they will be available via your package manager. The version of Pylux on 
the PyPI is outdated, instead install from the Git repository::

    git clone https://github.com/jackdpage/pylux.git
    cd pylux
    sudo python3 setup.py install

Content for Pylux is available from the `content repository`_.

If you are running an Arch derivative, a PKGBUILD is available for both at 
https://github.com/jackdpage/PKGBUILDs.

If you want to play sound cues, you will need to install mplayer.

.. _`content repository`: https://github.com/jackdpage/pylux-content

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
