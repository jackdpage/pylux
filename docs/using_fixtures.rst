Using Fixtures
==============

Fixtures are an important part of an effects plot. They represent a single 
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
create one from a template then edit from there::

    xN betapack2

This creates a new fixture from the ``betapack2`` template. This is an 
included fixture template with Pylux. You can also add your own fixture 
templates in ``~/.pylux/fixture/``.

Listing Fixtures
----------------

Now you can view your new fixture by running::

    xl

The following will be printed to your console::

    0 Zero88 Betapack 2 (Zero88 Betapack 2)

Setting Attributes
------------------

The name of this new fixture is ``Zero88 Betapack 2`` which is not very
useful if you have multiple fixtures of that type, so change the name by 
running:: 

    xs 0 name Top Dimmer

Now if you re-run ``xl``, you will see::

    0 Top Dimmer (Zero88 Betapack 2)

When using ``xs``, you can actually use any tag you like in place of ``name`` 
and that tag will be added to the data dictionary with the value you provide. 

Cloning Fixtures
----------------

Say you actually have two dimmerpacks, and you want to add another. You 
could run the ``xN`` command again, or you could make use of Pylux's 
cloning capabilitiy:: 

    xc 0

Now running ``xl`` gives you::

    0 Top Dimmer (Zero88 Betapack 2)
    1 Top Dimmer (Zero88 Betapack 2)

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
