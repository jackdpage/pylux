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

Clone the code and content repositories locally::

  git clone --recurse-submodules https://github.com/jackdpage/pylux.git
  
To get the absolute latest version of the content repository, update the submodule from the remote::

  git submodule update --remote --merge
  
Execute the pylux module from the repository root::

  python3 -m pylux

Pylux is written in pure Python 3. You will need the Python interpreter in order
to run it. Different interfaces and extensions require different dependencies. You can
run the majority of the program from the fallback interface, requiring no dependencies
at all. However it is recommended to at least install ``urwid`` to benefit from the CLI.

========= ============
Component Dependencies
========= ============
cli       urwid
report    jinja2
plot      numpy
========= ============

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
