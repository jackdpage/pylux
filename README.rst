Pylux
=====

Pylux is a program for creating and managing documentation for stage lighting.

Pylux currently has the capability to generate plaintext documentation from
Jinja template files and create 2D plots in SVG although you will need to provide 
your own fixture vector files.

You can also import data from an Eos ASCII export, including the complete patch,
groups, palettes, and cues.

Installation and Dependencies
-----------------------------
Pylux is available on PyPI, so after installing Python and pip, you can simply run::

    pip3 install pylux

The PyPI package does not include the content repository, which includes fixture
templates, symbols and documentation templates. Pylux will search in ``~/.pylux``
for this, so you can just clone the repository there::

    git clone https://github.com/jackdpage/pylux-content.git ~/.pylux

Simply run ``pylux`` from the terminal to launch the program.

Screenshot
----------
Screenshot of curses interface showing fixture list on the left and DMX universe summary 
on the right. Data imported directly from Eos ASCII export with no post-processing.

.. image:: https://i.ibb.co/jkGYtMb/sc.png

Sample Output
-------------
Rendered at 1:50 on A3

.. image:: https://i.ibb.co/DKQRLSD/plota3.png

Documentation
-------------

Documentation is available at
`Read the Docs`_.

.. _`Read the Docs`: http://pylux.readthedocs.org/

License
-------

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
