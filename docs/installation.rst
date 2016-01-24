Installation
============

Pylux is written in Python 3, so is naturally very easy to install. Before 
installing, however, you will need to get the Python 3 implementation for 
your platform. This is available from http://python.org. Alternatively, you 
can install all the Python dependencies from your package manager::

    sudo pacman -S python python-setuptools python-pip

Installing from the PyPI
------------------------

The simplest way of installing Pylux is from the PyPI::

    sudo pip install pylux

This will also install any other necessary dependencies which are available 
on the PyPI. Installing from the PyPI also gives you access to automatic 
updates by running::

    sudo pip install -U pylux

Installing from Source
----------------------

If you would rather install from source, the process isn't too dissimilar. 
You will still of course need to set up your environment in the same way, then 
clone the GitHub repository to get the latest source::

    git clone https://github.com/jackdpage/pylux.git

Once you have cloned the repository, change directory into the local 
repository, then run::

    python setup.py install

If you wish to update Pylux to a newer version in the future, you will have 
to pull from the GitHub remote, then re-run the setup script.
