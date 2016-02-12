Standard Tags
=============

The objects in Pylux, such as metadata and fixtures, all store information in 
the form of tags. A tag describes a piece of data (with no spaces, use an 
underscore if you need multiple words). The tag will then be assigned a value 
using a set command.

You can use any tags you using the set commands, however, they won't 
necessarily be useful. For that reason, there are some standard tags that are 
used by Pylux.

Standard Metadata Tags
----------------------

``production``
    The name of the production for which the documentation is being produced, 
    e.g. Romeo and Juliet

``designer``
    The name of the lighting designer for this production.

``board_operator``
    The name or list of names of the person or people who are operating the 
    lighting board for this production.

``spot_operator``
    The name or list of names of the person or people who are operating 
    followspots for this production.

``director``
    The name of the director of the production.

``venue``
    The location at which the production is taking place.

``stage_manager``
    The name of the stage manager for the production.


Standard Fixture Tags
---------------------

``dmx_channels``
    The number of DMX channels that this fixture requires to function 
    properly. This is calculated automatically based on the contents of the 
    ``dmx_functions`` list.

``dmx_start_address``
    Automatically set when addressing a fixture. The DMX start address of the 
    fixture.

``universe``
    Automatically set when addressing a fixture. The value of the ``universe`` 
    tag of the registry to which this fixture is addressed.

``posX``
    The x position in 2D space where this fixture is located. Measured in 
    metres relative to the centre line, where stage left is positive.

``posY``
    The y position in 2D space where this fixture is located. Measured in 
    metres relative to the plaster line, where downstage is positive.

``focusX``
    The x position in 2D space where the centre of this fixture's beam is 
    focused. Measured in metres relative to the centre line, where stage 
    left is positive.

``focusY``
    The y position in 2D space where the centre of this fixture's beam is 
    focused. Measured in metres relative to the plaster line, where 
    downstage is positive.

``circuit``
    For traditional fixtures only. The electrical circuit into which this 
    fixture is patched.

``power``
    For traditional fixtures only. The maximum power draw of the lamp in this 
    fixture.

``dimmer_uuid``
    For traditional fixtures only. The UUID of the dimmer (which must exist 
    as a separate fixture in the plot file) which is controlling this fixture.

``dimmer_chan``
    For traditional fixtures only. The name or number of the dimmer channel 
    by which this fixture is controlled.

``is_dimmer``
    Special tag set to ``True`` for dimmers.

``gel``
    The name or manufacturer's code of the gel that is being used in this 
    fixture. Certain gels allow for automatic colour calculation.

Pseudo Fixture Tags
-------------------

These tags cannot be set as tags for fixtures. They are instead used to set 
multiple other tags quickly and easily.

``position X,Y``
    Sets ``posX`` to ``X`` and ``posY`` to ``Y``.

``focus X,Y``
    Sets ``focusX`` to ``X`` and ``focusY`` to ``Y``.

``dimmer FIXTURE CHAN``
    Sets ``dimmer_uuid`` to the UUID of ``FIXTURE`` and ``dimmer_chan`` to 
    ``CHAN``.


Standard Cue Tags
-----------------

``type``
    The type of cue, either ``LX``, ``SX`` or ``VX``.

``location``
    The line or visual cue in the script at which this cue occurs.

``description``
    A human-readable description of what should happen when this cue occurs.

``scene``
    If this is a lighting cue, the UUID of the scene which is used for it.
