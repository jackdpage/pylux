The Plotter Context
===================

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

``pw PATH``
    Save the current SVG plot buffer to the location with path ``PATH``.

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

``show_beams``
    Choose whether or not to display beam focus lines. These are dashed lines 
    from the fixture to its focus point to assist with understanding where 
    fixtures are pointing. Must be ``True`` or ``False``. Default: ``True``

``beam_width``
    The thickness of the beam focus lines, in SVG points. Default: ``6``

``beam_colour``
    The colour of the beam focus lines. This can be any named gel colour in 
    the list of legal gel colours. Alternatively, it can be set to ``auto`` 
    to be the same colour as the fixture from which it originates. 
    Default: ``Black``
