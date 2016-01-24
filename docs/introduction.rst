Introduction
============

Pylux is a program written in Python whose primary purpose is the management 
of documentation for stage lighting. It could, however, just as easily be 
used for entertainment or event lighting.

The basis of Pylux is an XML file called a plot, which Pylux uses to store 
all the information about a specific lighting project. This file can contain 
a wide variety of information. Natively supported by Pylux are fixtures, 
DMX registries, cues and metadata.

From these files, Pylux can generate a variety of useful documentation. For 
example, Pylux can create any type of plaintext documentation using Jinja 
templates, or SVG diagrammatic representations of the lighting plot.
