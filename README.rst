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

Pylux is written in pure Python 3. You will need the Python interpreter in order
to run it. 

Clone the code and content repositories locally and update the content repository from the remote
to get the latest version::

  git clone --recurse-submodules https://github.com/jackdpage/pylux.git
  cd pylux
  git submodule update --remote --merge
  
Create an environment to run in and install dependencies from pip::

  python3 -m venv venv
  source venv/bin/activate
  pip3 install urwid jinja2 numpy pygdtf  
  
Execute the pylux module from the repository root::

  python3 -m pylux

Different interfaces and extensions require different dependencies. The 
program will automatically load components which you have dependencies installed for.

========= ============
Component Dependencies
========= ============
cli       urwid
report    jinja2
plot      numpy
template  pygdtf
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
