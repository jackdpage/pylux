The Plotter Context
===================

.. WARNING::
    The plotter context is currently being rewritten to comply with USITT
    standards. The information listed below is representative of the new 
    development version of plotter, which as accessible from the 
    plotterNEW context. These commands do not apply to the temporary plotter 
    implementation.

The plotter context is used to create 2D SVG images of the fixtures in the 
plot file. It uses the symbols defined by the ``symbol`` tag of fixtures to 
find SVG images of the fixtures. It then transforms these fixtures according 
to the position and focus tags. It also colours the fixtures according to 
their gel.

There are very few commands defined by plotter, there are, however, some 
additional options you can set before producing the SVG plots.

Commands
--------

``pn``
    Generate a new SVG plot from the current plot file and the options. This 
    will only store the file internally, if you wish to save the SVG image to 
    a file (which you probably do), you will need to run ``pw``

``pd``
    Mainly implemented for debugging purposes. Prints the SVG tree to the 
    console.

``pw PATH``
    Save the current SVG plot buffer to the location with path ``PATH``. 
    Pylux will automatically detect the desired file type based on the 
    extension of the path you provide. If the path ends in ``.svg``, Pylux 
    will write the XML (SVG) tree to the file. If the path ends in ``.pdf``, 
    Pylux will invoke ``cairosvg`` to convert the SVG to a PDF, then write 
    this to the file.

``ol``
    List the values of all the options that can be specified. These options 
    all have default values that you will see when you run the command.

``og NAME``
    Print the value of the option with name ``NAME``.

``os NAME VALUE``
    Set the value of the option with name ``NAME`` to ``VALUE``.


Options
-------

Use the option commands detailed above to change these options.


