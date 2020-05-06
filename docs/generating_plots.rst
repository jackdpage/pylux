Generating Plots
================

If you have SVG image files for your fixtures, you can create a 2D plot of
your rig. You need to have given all fixtures you wish to plot in the rig,
at minimum a posX and posY value. If you want them to be orientated correctly,
you will also need to give them either a rotation value or focusX and focusY values.

Create a new plot and save it in memory::

    Plot Create

Write the plot to disk::

    Plot Write output.svg

There are many many options you can change when creating a plot. You can see what they
are by running::

    Plot About

This will display the options in your Dynamic Output Pane. To change any of these, for
example scaling, run::

    Plot Set scale 25

You can also change the defaults in the program configuration file.

Customising the Plot
--------------------

The base defaults given in the configuration are optimised for the closest output to the
USITT standard possible. However, you can change these to suit your particular plot better.
You may find that some changes to these options require simultaneous changes to the default
stylesheet in order to maintain a cohesive look.

For boolean options, any boolean equivalent is acceptable, for example true, yes, 1, and on are all
acceptable in place of True.

Page Layout
^^^^^^^^^^^

``paper-size``
    The size of paper to fit the plot to. Accepted are ISO A[0-4]. Note, changing this option
    should be preferred to just scaling the entire plot to a different size after it has been converted
    to PDF. The ``paper-size`` attribute will ensure that line weights and font sizes are kept to
    standard, and also dynamically resizes the title block based on the paper size. Default ``A3``.
``orientation``
    Specify landscape or portrait. Default ``landscape``.
``margin``
    Leave spacing between the edge of the paper and print area. No fixtures will be drawn outside
    this margin. Some other components may extend beyond the margin if they are set to do so.
    Measured in millimeters. Default ``10``.
``page-border``
    Draw a black border around the page. This is drawn inside the margin. Default ``True``.

Drawing Options
^^^^^^^^^^^^^^^

``scale``
    The scale at which to produce the plot. Only metric scales are acceptable, although this
    number can be a decimal. Default ``50``.
``plaster-line-padding``
    By default, the centre of the plot area is the intersection of the plaster line and centre
    line. You can however offset the centre vertically through this option. Positive numbers will
    increase the area visible in the positive y direction. i.e. the plaster line will be
    moved down in the output. Measured in unscaled metres. Default ``0``.
``background-image``
    A path to an vector file which is placed on the drawing surface before anything else. This
    image must be in the prescribed format and centred about the plaster line / centre line
    intersection. Default ``plot_background.svg``.
``line-weight-light``, ``line-weight-medium``, ``line-weight-heavy``
    The plot is based on a three-weight drawing, as prescribed by the USITT standard. Refer
    to section 6.18 of the standard for which each weight is used for. In addition to this,
    ``line-weight-light`` is also used for any general components. Measured in millimeters.
    Defaults ``0.4``, ``0.6``, ``0.8``
``style-source``
    A path to an external CSS file, which defines necessary external styling for both the SVG
    file itself and the foreignObject HTML injections inside it. Primarily used for text
    formatting. A default style file is provided with the installation, which can be freely
    edited by the user. Default ``style.css``.
``centre-line-dasharray``, ``plaster-line-dasharray``
    An SVG dasharray specification to use for the centre and plaster lines. The default is designed to
    closely match the USITT specification. Defaults ``4, 0.5, 1, 1.5``, ``3, 0.7``.
``centre-line-extend``, ``plaster-line-extend``
    When set to True, the centre and plaster lines will printed beyond the page border into
    the margin, to the extent of the actual paper. Defaults ``False``.

Fixture Icon Options
^^^^^^^^^^^^^^^^^^^^

``fallback-symbol``
    Plot will attempt to draw every fixture with position values, even if they do not have a
    symbol. Specify here the symbol that should be used in the event that the fixture does
    not have a symbol tag. Default ``Generic/Parcan``.
``colour-fixtures``
    If set to True, fixtures will be coloured in according to their gel tag. Any gels which
    can't be converted to RGB, or any fixtures without a gel tag, will be displayed in the
    default of white. This colouring is applied to all parts of the fixture icon with the
    ``outer`` class, whilst white is applied to all parts with the ``inner`` class.
    Default ``False``.

Additional Component Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``show-channel-number``, ``show-circuit-number``, ``show-dimmer-number``
    These can be toggled in any combination to specify whether the fixture's channel, circuit
    and dimmer numbers should be displayed next to the fixture icon in the USITT format. Refer
    to section 6.14.1 of the standard to see what this is. The additional information will only
    be displayed if it appears in the fixture in ``circuit`` or ``dimmer`` tags. The fixture
    reference is always assumed to be the channel number so will always be printed if this option
    is enabled. Default ``True``.
``channel-notation-radius``
    Each of the channel, circuit and dimmer numbers are printed in a box as given by the
    standard. Use this option to change the nominal size of the boxes. Measured in
    millimetres. Default ``3.1``.
``notation-connectors``
    If disabled, will prevent the connector lines between the fixture body and external notation
    numbers (channel, circuit, dimmer) from being draw. Default ``True``.
``show-beams``
    If enabled, a line will be printed from the centre of the fixture to it's focus position.
    A fixture must have both ``focusX`` and ``focusY`` tags for this to display. In the event that
    the focus point is outside of the drawing area, beam lines will extend beyond the border
    into the margins. Default ``False``.
``beam-dasharray``
    An SVG dasharray specification for the aforementioned fixture beams. Default ``1, 1``.
``beam-source-colour``
    If enabled, the beam lines will be printed in the colour matching the source fixture's
    gel tag. Inconvertible gel names or fixtures without gels will continue to have their
    beams rendered in black. Default ``False``.
``show-focus-point``
    Draws a circle at the focus position of each fixture. Similar to the beams option. These
    will only work on fixtures with focus values and will print in the margins. Default ``False``.
``focus-point-radius``
    Adjust the radius of the drawn focus point circle. Measured in millimeters. Default ``1``.
``focus-point-source-colour``
    Similar to the ``beam-source-colour`` option, if enabled, focus points will be rendered
    according to the colour of the gel in the source fixture. Default ``False``.

Title Block Format
^^^^^^^^^^^^^^^^^^

``title-block``
    What format of title block to use. Currently supported formats are ``None`` and ``sidebar``.
    ``None`` will omit the title block entirely. ``sidebar`` will draw the title block down the
    full height on the right hand side of the page.
``sidebar-title-width-pc``, ``sidebar-title-min-width``, ``sidebar-title-max-width``
    The width of the sidebar title is calculated as a percentage of the page width, defined
    by ``sidebar-title-width-pc``. Minimum and maximum widths, in millimetres can be provided
    to ensure that sidebar titles remain sensible widths when changing the paper size.
    Defaults ``0.1``, ``50``, ``100``.
``titles``
    A list of metadata tags to include in the title section of the title block. These are
    added to an HTML foreignObject element for external styling with the included stylesheet.
    Only the tag values are added, headings should be added using the ::before CSS selector.
    Class names given to the text paragraph will be ``title-meta_tag_name``. Format as a
    literal list of strings. Default ``['company', 'production', 'venue', 'lighting_designer']``
``sidebar-icon-width-factor``
    In a sidebar title block, the fixture icon legend is shown as a vertical list. This setting
    determines the proportion of the width of the sidebar which will contain the icon, whilst
    the remainder will be occupied by the label text. For example, a value of ``4`` will mean
    that 100/4 = 25% of the sidebar width will be the icon itself and the remaining 75% will be
    the label for the legend. This will require adjustment if you are changing the scale and
    have fixtures whose geometric centres are not equivalent to their hanging points. Default ``3.2``.
