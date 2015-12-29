# Pylux

Pylux is a suite for the management of lighting documentation. Currently, the 
package includes two programs: ``plotter``, for the manipulation of Pylux's 
XML formatted plot files and ``texlux``, for the production of LaTeX reports 
from Pylux plot files.

``plotter`` currently is only functional on the CLI, but a GUI is in 
development.

## Installation and Dependencies

Pylux is written in Python 3, so Python 3 must be installed. Run the setup 
script to install the necessary Python binaries and also additional files 
which are packaged with Pylux: ``sudo python setup.py install``.

TeXlux does not require LaTeX to be installed to produce the reports, as they 
are produced as LaTeX source, however, you will need a LaTeX distribution, such 
as TeX Live, installed in order to build PDF files from this source.

## Contributing

If you know Python, XML, LaTeX or English, you can contribute by:

+ Writing code (in Python);
+ Making new fixture files (in XML);
+ Writing documentation (in LaTeX);
+ Submitting bug reports and feature requests (in English).

Pylux is (almost) fully documented using docstrings, meaning you can find most 
of the documentation you will need by running ``pydoc``. Refer to ``TODO.txt`` 
to see what needs to be done.

Please submit any bug reports or feature requests to the GitHub issues tracker. 

Anything else should be edited on a fork then a pull request submitted.

## License

Pylux is licensed under the GNU GPL v3.0. A full copy of the license is 
available in the file ``COPYING``.
