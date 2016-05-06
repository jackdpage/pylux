The Editor Context
==================

The editor context is used to directly edit the content of the XML files that 
Pylux uses to store information about a plot.

There are a great number of commands available in the editor context, which 
have been split below based on object.

File Commands
-------------

You can only edit one plot file at a time in Pylux. Also, there is no 
autosaving feature so you must remember to run ``fw`` regularly.

``fo file``
    Open the file with path ``file`` as the plot file. This will override any 
    unsaved buffer associated with the previous plot file, if there was one.

``fw``
    Save the plot file buffer to the location from which the current plot file 
    was loaded.

``fW path``
    Save the plot file buffer to the location with path ``path``.

``fg``
    Print the path of the plot file which is currently loaded.

``fs path``
    Set the default save location for the current plot file buffer to the 
    location with path ``path``.

Metadata Commands
-----------------

These commands manipulate the metadata objects in a plot file.

``ml``
    List all metadata tags and their values.

``ms META value``
    Set the value of the metadata item ``META`` to ``value``.

``mr META``
    Remove metadata item ``META``.

``mg tag``
    Print all the values of metadata that have the tag ``tag``.

Fixture Commands
----------------

Fixtures are the most fundamental concept in the plot file, and are necessary 
to have a functional, useful environment.

``xn name``
    Creata a new fixture from scratch with name ``name``. All other fields 
    will be blank and the fixture will have no DMX functions associated with 
    it. A new UUID is assigned.

``xN template``
    Create a new fixture and load the contents of the fixture template file 
    ``template`` into it. Fixture template files should specify ``%UUID%`` in 
    place of UUIDs to allow for automatic generation. Some fixture templates 
    are included, others should be placed in ``~/.pylux/fixture/``.

``xc FIXTURE``
    Create a new fixture and load the contents of an existing fixture into 
    it, including any DMX functions and user-defined data. A new UUID is 
    assigned.

``xl``
    List all fixtures in the plot file. Lists name, type and assigns 
    interface references.

``xf tag value``
    List fixtures whose value of ``tag`` in their data dictionary is 
    ``value``. Prints name and assigns interface references.

``xg FIXTURE``
    Print the value of every data tag that is assigned to ``FIXTURE``.

``xG FIXTURE``
    Print the value of every data tag that is assigned to ``FIXTURE``, and 
    also list the functions of the fixture. Interface references are given to 
    functions.

``xr FIXTURE``
    Remove ``FIXTURE`` from the plot file. Any associated DMX channels will 
    remain. To remove these at the same time, use the ``xp`` command.

``xs FIXTURE TAG VALUE``
    Set the value of the tag with name ``TAG`` to ``VALUE`` for ``FIXTURE``.

``xa FIXTURE universe addr``
    Assign DMX addresses to ``FIXTURE``. This will assign a new channel in the 
    registry with universe name ``UNIVERSE`` for each DMX function defined by 
    the fixture. It will start assigning values at address number ``ADDR`` or, 
    if ``ADDR`` is ``auto``, the next best start address based on the 
    available free channels.

``xA FIXTURE``
    Unassign all DMX addresses associated with the functions of ``FIXTURE``, 
    in all universes.

``xp FIXTURE``
    Purge ``FIXTURE``. This acts much like the ``xr`` command, except it also 
    removes any associated DMX information from the necessary registries.

DMX Registry Commands
---------------------

DMX registries store information about which fixtures are controlled by 
certain DMX addresses in a certain universe.

``rl UNIVERSE``
    List the used channels in the registry with universe name ``UNIVERSE``. 
    This will list both the fixture name and the function of the channel. 
    Sample output::

        001 Betapack 1 (channel_1)
        002 Betapack 1 (channel_2)
        003 Betapack 1 (channel_3)
        003 Betapack 2 (channel_1)
        004 Betapack 1 (channel_4)
        004 Betapack 2 (channel_2)
        005 Betapack 1 (channel_5)
        005 Betapack 2 (channel_3)
        006 Betapack 1 (channel_6)
        006 Betapack 2 (channel_4)
        007 Betapack 2 (channel_5)
        008 Betapack 2 (channel_6)

``rL UNIVERSE``
    List the used channels in the registry with universe name ``UNIVERSE``, 
    and also probe any dimmer channels to display the fixtures they control. 
    Sample output::

        001 Betapack 1 (channel_1)
        002 Betapack 1 (channel_2)
        003 Betapack 1 (channel_3)
            ⤷ Hutton P650
        003 Betapack 2 (channel_1)
            ⤷ PAR64 MFL
        004 Betapack 1 (channel_4)
        004 Betapack 2 (channel_2)
        005 Betapack 1 (channel_5)
        005 Betapack 2 (channel_3)
        006 Betapack 1 (channel_6)
        006 Betapack 2 (channel_4)
        007 Betapack 2 (channel_5)
        008 Betapack 2 (channel_6)


Cue Commands
------------

Cues are specifically designed for use in theatre. They contain information 
about the lighting state at a certain point in a script. This information 
could be a directive to an operator or specific DMX information.

``qn TYPE LOCATION``
    Append a cue to the cue list. Sets the type of cue to ``TYPE``, where 
    ``TYPE`` is either ``LX``, ``SX`` or ``VX``. Also sets the value of the 
    ``location`` tag to ``LOCATION``, which should be the line or visual in 
    the script at which this cue occurs. This also assigns a sort key to the 
    cue such that it appears after every other cue that has been added 
    previously.

``ql``
    List all the cues in the plot file. This lists the type, location and 
    sort key of the cue. The sort key can be considered to be an interface 
    reference for the purpose of piping cues into other commands.

``qs CUE TAG VALUE``
    Set the value of the tag with name ``TAG`` to ``VALUE`` in ``CUE``.

``qg CUE TAG``
    Print the value of the tag with name ``TAG`` in ``CUE``.

``qG CUE``
    Print the value of all tags that have been assigned to ``CUE``.

``qr CUE``
    Remove ``CUE`` from the plot file.

``qm CUE DEST``
    Adjust the sort keys of any necessary cues so that ``CUE`` comes 
    immediately after the cue ``DEST`` in the cue list.

``qM CUE DEST``
    Adjust the sort keys of any necessary cues so that ``CUE`` comes 
    immediately before the cue ``DEST`` in the cue list.
