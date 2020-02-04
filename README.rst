Pylux
=====

Pylux is a program for creating and managing documentation for stage lighting.

Pylux currently has the capability to generate plaintext documentation from
Jinja template files and create 2D plots in SVG although you will need to provide
your own fixture vector files.

You can also import data from an Eos ASCII export, including the complete patch
(excluding multicell fixtures), groups, and cues.

Installation and Dependencies
-----------------------------

Pylux is written in pure Python 3. You will need the Python interpreter in order
to run it. You will also need a few dependencies, which can be installed using pip::

    pip3 install urwid jinja2


Documentation
-------------

Documentation is available at
`Read the Docs`_.

.. _`Read the Docs`: http://pylux.readthedocs.org/

License
-------

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
