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

There are many options which you can change to alter the appearance of your 
plot. These options all have sane defaults in the config file. You can edit 
them either for all your projects in the config file at 
``~/.pylux/settings.conf`` or you can edit them on a temporary basis using the 
option commands listed above.

``paper-size``
    The ISO name of the paper you are using. Must be A[0-4]. Default: A4.

``orientation``
    The orientation of the printed plot. Must be landscape or portrait. 
    Default: landscape.

``margin``
    Margin to leave unprinted on all four sides of the paper. Measured in 
    millimetres. Default: 10.

``scale``
    The scale to use for the drawing. Default: 50.

``line-weight-light``
    Line weight for light lines (scenery, leader lines, dimensions). Measured 
    in millimetres. Default: 0.4.

``line-weight-medium``
    Line weight for medium lines (masking, drops, centre line, plaster line). 
    Measured in millimetres. Default: 0.6.

``line-weight-heavy``
    Line weight for heavy lines (batten, fixture, architecture, drawing 
    border, title block border). Measured in millimetres. Default: 0.8.

``title-block``
    If and where to display the title block. Must be corner, sidebar or None. 
    Default: corner.

``vertical-title-width-pc``
    If sidebar title is selected, the width of it as a percentage of the 
    page width. Default: 0.1.

``vertical-title-min-width``
    If sidebar title is selected, the minimum width it will render as. 
    Measured in millimetres. Default: 50.

``vertical-title-max-width``
    If sidebar title is selected, the maximum width it will render as.
    Measured in millimetres. Default: 100.

``corner-title-width-pc``
    If corner title is selected, the width of it as a percentage of the 
    page width. Default: 0.25.

``corner-title-height-pc``
    If corner title is selected, the height of it as a percentage of the 
    page height. Default: 0.25.

``corner-title-min-width``
    If corner title is selected, the minimum width it will render as.
    Measured in millimetres. Default: 70.

``corner-title-max-width``
    If corner title is selected, the maximum width it will render as.
    Measured in millimeters. Default: 120.

``corner-title-min-height``
    If corner title is selected, the minimum height it will render as.
    Measured in millimetres. Default: 40.

``corner-title-max-height``
    If corner title is selected, the maximum height it will render as.
    Measured in millimetres. Default: 80.

``centre-line-dasharray``
    The SVG dasharray property of the centre line. Default corresponds to 
    USITT standards. Must be a valid SVG dasharray value. 
    Default: 4, 0.5, 1, 1.5.

``centre-line-extend``
    Whether or not the centre line should extend over the page margins. 
    Must be True or False. Default: False.

``plaster-line-dasharray``
    The SVG dasharray property of the plaster line. Default corresponds to 
    USITT standards. Must be a valid SVG dasharray value. Default: 3, 0.7.

``plaster-line-extend``
    Whether or not the plaster line should extend over the page margins. Must 
    be True or False. Default: False.

``plaster-line-padding``
    The physical distance to be left upstage of the plaster line to allow 
    space for scenery, etc. Measured in metres. Default: 0.5.
