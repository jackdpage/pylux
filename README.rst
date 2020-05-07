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

Clone the code and content repositories locally::

  git clone --recurse-submodules https://github.com/jackdpage/pylux.git
  
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
========= ============

Documentation
-------------

Documentation is available at
`Read the Docs`_.

.. _`Read the Docs`: http://pylux.readthedocs.org/

License
-------

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
