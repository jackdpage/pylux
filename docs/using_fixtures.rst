Using Fixtures
==============

Fixtures are an important part of a plot. They represent a single
physical lighting instrument and are used to create plot drawings and 
hanging documentation.

Fixtures contain quite a bit more information than metadata: they consist of 
a data dictionary and a DMX functions list. The data dictionary is simply 
a key/value list of information about the fixture. The DMX functions list 
is actually a subvalue of the dictionary and describes how the fixture can be
controlled by the DMX protocol.

Creating Fixtures
-----------------

Because of the complexity of fixtures, especially those that contain DMX 
functions, it is not recommended to create them from scratch. Instead, 
create one from a template then edit from there::

    xN auto Generic/PAR64 MFL

This creates a new fixture from the ``Generic/PAR64 MFL`` template. This is an
included fixture template with Pylux.

Listing Fixtures
----------------

Now you can view your new fixture by running::

    xl

The following will be printed to your console::

    1 PAR64 MFL - Unnamed

Setting Attributes
------------------

By default fixtures do not have names, but it may be useful to give them a
label so they are easily identifiable when you have many fixtures of the same
type::

    xs 1 name SL pipe end

Now if you re-run ``xl``, you will see::

    1 PAR64 MFL - SL pipe end

When using ``xs``, you can actually use any tag you like in place of ``name`` 
and that tag will be added to the data dictionary with the value you provide.

Reserved Attributes
~~~~~~~~~~~~~~~~~~~

These attributes are regularly set automatically based on other attributes,
therefore they should not be used as they will be overwritten:

* ``colour`` overwritten based on the contents of ``gel``
* ``focusX`` ``focusY`` ``focusZ`` overwritten based on ``focus``
* ``posX`` ``posY`` ``posZ`` overwritten based on ``pos``
* ``rotation`` overwritten based on ``focus`` and ``pos``

Cloning Fixtures
----------------

Say we have five more PAR cans that we wish to add, we can use the cloning
command to quickly add these between references 2 and 6::

    xc 1 2:6

Notice that whenever you supply a unique reference, you can usually supply a
range of references to run the command in bulk.

Now running ``xl`` will display all six fixtures which have been added.

You can now rename fixture *1* using the ``xs`` command again.

Getting Fixture Information
---------------------------

If you would like to know more about one of the fixtures in your effects 
plot, you can either run ``xg`` to list all the data tags that fixture has 
or ``xG`` to list data tags and DMX functions. For example:: 

    xg 0

This command prints the following::

    Top Dimmer
    2 Data Tags:
        type: Zero88 Betapack 2
        isDimmer: True

Alternatively run:: 

    xG 0

This then prints the following::

    Top Dimmer
    2 Data Tags:
        type: Zero88 Betapack 2
        isDimmer: True
    6 DMX Functions:
        0 Channel 1
        1 Channel 2
        2 Channel 3
        3 Channel 4
        4 Channel 5
        5 Channel 6

Assigning DMX Addresses to Fixtures
-----------------------------------

The data patching a fixture function to a DMX address exists in Registry
objects, although it is a fixture command which is used to assign these
addresses.

You will need to create a registry object for each universe you use::

    rn 0

