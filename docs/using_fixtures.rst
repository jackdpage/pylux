Using Fixtures
==============

Fixtures are an important part of the show file. They represent a single
physical lighting instrument and are used to create plot drawings and 
hanging documentation.

Fixtures contain quite a bit more information than metadata: they consist of 
a data dictionary and a DMX functions list. The data dictionary is simply 
a key/value list of information about the fixture. The DMX functions list 
describes how the fixture can be controlled by the DMX protocol.

Creating Fixtures
-----------------

Because of the complexity of fixtures, especially those that contain DMX 
functions, it is not recommended to create them from scratch. Instead, 
create one from a template then edit from there.

Pylux supports the General Device Type Format (GDTF) developed by Robe, MA
and Vectorworks for creating fixtures from templates. A wide range of fixture
types can be downloaded from gdtf-share.com, where there is also an interactive
builder to create your own templates. To create a new fixture from one::

    Fixture 1 CreateFrom Robe_lighting_s.r.o.@Robin_Spikie@24062020

This creates a fixture from the file
``Robe_lighting_s.r.o.@Robin_Spikie@24062020.gdtf``. 1 is the reference given
to this new fixture.

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

    Fixture 1 Label SL pipe end

Now you will see your fixture has the label SL pipe end, when using both Display and About.

In addition to a label, fixtures can hold any kind of information you like with
an arbitrary key/value structure. For example, to indicate a gel of LEE 102::

    Fixture 1 Set gel L102

To remove an attribute from a fixture, just use the Set command without a value::

    Fixture 1 Set gel

Cloning Fixtures
----------------

Say we have five more Spikies that we wish to add, we can use the cloning
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

    Fixture 1>6 Patch 0 0

This will patch your fixtures in universe 0 at address 0. Of course address 0
does not exist, 0 in this case means, the next available set of addresses where
this fixture will fit. This is obviously 1 in this case.

The program will automatically create the required registry object for you.

Using Fan
---------

Fan allows you to set an attribute to different levels across a range of
fixtures with a single command. In order for this to work, you must provide a
numeric start and end value for the program to interpolate between. This is
especially useful for setting the position of fixtures.

Using the example above, let's assume our six Spikies are rigged on a lateral
batten at Y=1.0m and are evenly spaced between X=-5.0m and X=5.0m. We can set
all of these values using just two commands::

    Fixture 1>6 Set posY 1
    Fixture 1>6 Fan posX -5 5
Note Fan will always operate in document order and ignore the the actual
provided order of fixtures on the command line.