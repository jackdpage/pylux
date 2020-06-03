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
create one from a template then edit from there.

Pylux supports two types of template, General Device Type Format (GDTF) and its
own JSON format. The default and preferred format is GDTF. Create a fixture from
an existing template::

    Fixture 1 CreateFrom Generic@Parcan

This creates a fixture from the file ``Generic@Parcan.gdtf``. Pylux assumes that any
template given without a file extension is a GDTF file. Alternatively, to create the
fixture from the JSON template::

    Fixture 1 CreateFrom Generic/Parcan.json

1 is the reference given to this new fixture.

Displaying Fixtures
-------------------

You will have seen the fixture appear in the Fixed Output Pane if you are in the
Fixture context. You can also show the fixture in the Dynamic Output Pane by running::

    Fixture 1 Display

If you want a bit more information on the fixture, such as additional data tags and
DMX functions, you can run::

    Fixture 1 About

Setting Attributes
------------------

By default fixtures do not have names, but it may be useful to give them a
label so they are easily identifiable when you have many fixtures of the same
type::

    Fixture 1 Set label SL pipe end

Now you will see your fixture has the label SL pipe end, when using both Display and About.

In place of ``label``, you may put any arbitrary tag you like, such as ``gel``, ``posX`` etc.
For a list of suggested and reserved attributes, see the appendicies.

Cloning Fixtures
----------------

Say we have five more PAR cans that we wish to add, we can use the cloning
command to quickly add these between references 2 and 6::

    Fixture 1 CopyTo 2>6

Notice that whenever you supply a unique reference, you can usually supply a
range of references to run the command in bulk.

Get information about all of these by running::

    Fixture * About

Assigning DMX Addresses to Fixtures
-----------------------------------

The data patching a fixture function to a DMX address exists in Registry
objects, although it is a fixture command which is used to assign these
addresses::

    Fixture 1 Patch 0 0

This will patch your fixture in universe 0 at address 0. Of course address 0
does not exist, 0 in this case means, the next available set of addresses where
this fixture will fit. This is obviously 1 in this case.

The program will automatically create the required registry object for you.