Using Metadata
==============

Metadata is by far the simplest data type available to you in Pylux, so it 
makes sense to begin the documentation with an example on how to use it.

Metadata essentially consists of two attributes: a key and a value. When 
you create a piece of metadata you must supply the key; the value is given 
later using a different command.

First create a piece of metadata. For this example, we'll set the name of the 
director for this production::

    mn auto Director

This creates a new metadata object with an automatic unique reference. You
could have instead written any integer in place of auto.

    ml

This translates to *metadata list*. You will then see the following printed 
to your console::

    1 Director: Empty

Because you didn't have any metadata in your plot file yet, the new metadata
was automatically assigned a reference of 1.

Your metadata doesn't have a value yet, so it's meaningless. There is another 
command for setting the value of a piece of metadata::

    ms 1 J. Smith

This translates to *metadata set [data with reference] 1 [to] J. Smith*.
Notice that in order to set the value of the metadata we just made, we 
supply the integer that is displayed next to it on the screen when we ran 
the ``ml`` command. You must always supply the unique reference when you are
editing Pylux objects.

Say you wanted to remove the metadata, you would run::

    mr 1

This translates to *metadata remove [data with reference] 0*.
