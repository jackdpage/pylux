The Plot Module
===============

The plot module is the module in which you will find the majority of the 
functionality of Pylux. This module calls upon the ``xml.etree.ElementTree`` 
module to parse the XML files into Python-readable objects, then turns these 
into slightly nicer, more accessible objects that can be easily used by any 
other Pylux modules.

The PlotFile Class
------------------

The PlotFile class deals with the loading and initial parsing of the plot 
file. It defines some basic methods that are primarily used by the ``editor`` 
context to perform standard file functions.

Attributes
^^^^^^^^^^

In general, these attributes should not be accessed outside of the class. 
They are available for use but wherever possible you should use one of the 
methods provided or another class.

``file``
    The path of the plot file.

``tree``
    The parsed XML tree, an object defined by ``xml.etree.ElementTree``. This 
    is often referred to as the buffer by this documentation.

``root``
    The root element (``plot``) of the XML tree.

Methods
^^^^^^^

``load(path)``
    Loads the file at the location with path ``path`` as the plot file. Note 
    you can only have a single plot file loaded at a time, so this will 
    discard the buffer of the previous file.

    Arguments

    ``path``
        The path from which to load the plot file.
