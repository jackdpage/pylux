Using Metadata
==============

Metadata is by far the simplest data type available to you in Pylux, so it 
makes sense to begin the documentation with an example on how to use it.

Metadata essentially consists of two attributes: a key and a value. When 
you create a piece of metadata you must supply the key; the value is given 
later using a different command.

First create a piece of metadata. For this example, we'll set the name of the 
director for this production::

    mn Director

This command simply translates to *metadata new [with key] Director*. You 
can see the piece of metadata you created by running::

    ml

This translates to *metadata list*. You will then see the following printed 
to your console::

    0 Director: 

Your metadata doesn't have a value yet, so it's meaningless. There is another 
command for setting the value of a piece of metadata::

    ms 0 J. Smith

This translates to *metadata set [data with reference] 0 [to] J. Smith*. 
Notice that in order to set the value of the metadata we just made, we 
supply the integer that is displayed next to it on the screen when we ran 
the ``ml`` command. This is called an **interface reference**, and they are 
used extensively by Pylux for moving more complex data types around.

Say you wanted to remove the metadata, you would run::

    mr 0

This translates to *metadata remove [data with reference] 0*.
