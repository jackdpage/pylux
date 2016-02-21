#!/usr/bin/python3.5
"""Install Pylux."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylux',
    version='0.2.1',
    description='A program for managing lighting documentation.',
    long_description=long_description,
    url='http://os.pwrg.uk/software/pylux',
    author='Jack Page',
    author_email='jdpboc98@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: Office/Business',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3.5',
    ],
    keywords='lighting theatre stage tech',
    packages=['pylux', 'pylux.context'],
    install_requires=['tabulate', 'Jinja2', 'cairosvg'],
    package_data={
        'pylux': ['settings.conf', 
                  'fixture/*.xml', 
                  'template/*', 
                  'symbol/*.svg']
    },
    entry_points={
        'console_scripts': [
            'pylux=pylux.__main__:main',
        ],
    },
)
