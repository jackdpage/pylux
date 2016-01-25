The Reporter Context
====================

The reporter context is a very powerful context that can any type of plaintext 
documentation from Jinja template files.

Commands
--------

``rn TEMPLATE OPTIONS``
    Create a new report using the template with name ``TEMPLATE`` and pass 
    the list of options, ``OPTIONS`` to the template.  This will 
    search the normal Pylux directories for any file with the name 
    (excluding any extension) ``TEMPLATE``. If more than one template is 
    found with the same name but different extensions, a list will be printed 
    of all found templates, and then a prompt displayed for you to select one 
    of them. Much like ``pn`` in the plotter context, this does not save the 
    report to a file, only internally. You will need to use ``rw`` to save it 
    to a file.

``rg``
    Print the internal report buffer.

``rw PATH``
    Save the internal report buffer to the location with path ``PATH``.

Options
-------

Some templates may choose to define some additional options that the user can 
define when the report generation is run. These are specified using a 
``key=value`` syntax in a comma-separated list after the ``rn`` command.

The allowable options are completely dependent on the template being used. 
The documentation for the template should make clear what they are. For 
example, an HTML template may allow you to select the styling::

    rn cuelist style-base=milligram,style-mode=night
