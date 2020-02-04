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