Importing Data
==============

Pylux allows you to import data from external sources. Currently, there is 
support for importing information from USITT ASCII files, with support for 
some ETC Eos extensions.

Use the ``ia`` command to import target data from a specified file::

  ia source data_type

Where ``source`` is the path to your exported ASCII file, relative to 
where Pylux was launched from and ``data_type`` is the type of information 
that you wish to read from the file. The different potential data types 
are explained below.

Conventional patch
------------------

Specifying ``conventional_patch`` as your data type will only import lines 
of conventional USITT patch. These are all single-channel fixtures and will be 
imported as the default type specified in the configuration file. By default 
this is ``Generic/Dimmer``. New registries will be created automatically if 
addresses exist in universes that have not yet been created.

Eos patch
---------

Specifying ``eos_patch`` will read Eos-specific ``$Patch`` lines that include 
support for advanced personalities and fixture information. Pylux will search 
through personalities in the ASCII file and attempt to convert these into the 
internal JSON format where possible. Fixtures will then be patched, including 
assigning UUIDs to DMX functions.

Eos patch will also read the Text field and assign this to the ``label`` tag 
of the fixture. Similarly the Gel field will be assigned to the ``gel`` tag.

Cues
----

The ``cues`` data type will import conventional USITT cues, containing 
intensity information only. Cues with the specified references will be created 
and label, up time and down time assigned where possible.

Levels for each fixture are set using the internal ``cue_set_fixture_level`` 
command, which automatically determines the intensity channel and populates 
this in the cue levels dictionary. This will take the first instance of a 
function named ``Intens`` and therefore may not work properly for fixtures 
with multiple intensity parameters. 
