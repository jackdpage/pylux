Editor Reference
================

Editor is the default context in Pylux and is used for directly editing 
most of the contents of the effects plot.

Metadata Commands
-----------------

metadata_list
^^^^^^^^^^^^^
Usage
    ``ml``
Affects Buffers
    *MET*
Synopsis
    List all the metadata objects in the effects plot file.

metadata_get
^^^^^^^^^^^^
Usage
    ``mg name``
Affects Buffers
    *MET*
Parameters
    *name* - the name to match against existing metadata.
Synopsis
    List all the metadata objects in the effects plot file whose name 
    matches *name*.

metadata_new
^^^^^^^^^^^^
Usage
    ``mn name``
Parameters
    *name* - the name to assign to the newly created metadata.
Synopsis
    Create a new piece of metadata in the effects plot and give it the name 
    *name*.

metadata_set
^^^^^^^^^^^^
Usage
    ``ms MET value``
Parameters
    *MET* - the item of metadata of which the value is to be changed.

    *value* - the new value to assign to the metadata.
Synopsis
    Change the value of an existing piece of metadata *MET* to *value*.

metadata_remove
^^^^^^^^^^^^^^^
Usage
    ``mr MET``
Parameters
    *MET* - the item of metadata to remove from the effects plot.
Synopsis
    Completely remove an existing piece of metadata from the effects plot.

Fixture Commands
----------------

fixture_list
^^^^^^^^^^^^
Usage
    ``xl``
Affects Buffers
    *FIX*
Synopsis
    List all the existing fixtures in the effects plot. This command will 
    display the fixture's name and type.

fixture_filter
^^^^^^^^^^^^^^
Usage
    ``xf tag value``
Affects Buffers
    *FIX*
Parameters
    *tag* - the data tag of the fixtures to test.

    *value* - the value to match the fixture's data tags against.
Synopsis
    List all the fixtures in the effects plot who have a data tag called 
    *tag*, the value of which is equal to *value*.

fixture_get
^^^^^^^^^^^
Usage
     ``xg FIX``
Parameters
     *FIX* - the fixture to print the data tags of.
Synopsis
     List all the data tags associated with a fixture, including those 
     added automatically by Pylux.

fixture_getall
^^^^^^^^^^^^^^
Usage
     ``xG FIX``
Affects Buffers
     *FNC*
Parameters
     *FIX* - the fixture to print the data tags and DMX functions of.
Synopsis
     List all the data tags associated with a fixture as per fixture_get, 
     but also list any DMX functions the fixture has associated with it.

fixture_new
^^^^^^^^^^^
Usage
     ``xn name``
Parameters
     *name* - human-readable name to give to the fixture.
Synopsis
     Create a new fixture object from scratch. The only attribute of the 
     created fixture will be its name. Usage of this command is not 
     recommended as it does not allow for DMX function assignment.

fixture_from_template
^^^^^^^^^^^^^^^^^^^^^
Usage
     ``xN template``
Parameters
     *template* - the name of the template to load into this new fixture.
Synopsis
     Create a new fixture from an existing template file. The root directory, 
     ``/usr/share/pylux/fixture`` and home directory, ``~/.pylux/fixture`` 
     are both searched to find a fixture template called *template*.xml. If 
     a template with the same name is found in both locations, the template 
     in the home directory is preferred. See the creator documentation for 
     more information on creating fixture templates.

fixture_clone
^^^^^^^^^^^^^
Usage
     ``xc FIX``
Parameters
     *FIX* - the existing fixture to make a copy of.
Synopsis
     Create a new fixture and populate its data dictionary and DMX functions 
     list with the contents of an existing fixture. New UUIDs are created so 
     the new fixture is not linked to the existing fixture.

fixture_set
^^^^^^^^^^^
Usage
     ``xs FIX tag value``
Parameters
     *FIX* - the fixture of which the data dictionary is to be changed.

     *tag* - the name of the tag to set the value of.

     *value* - the new value to assign to the tag.
Synopsis
     Set the value of a new or existing data tag in the fixture's data 
     dictionary. Tags must be one word, it is recommended to use 
     lowerCamelCase where more than one word is required, to maintain 
     consistency with standard Pylux tags.

fixture_address
^^^^^^^^^^^^^^^
Usage
     ``xa FIX REG start``
Parameters
     *FIX* - the fixture who's functions are to be assigned addreses.

     *REG* - the registry to assign addresses in.

     *start* - the address to begin registration at. Set to auto to allow 
               Pylux to choose the best start address.
Synopsis
     Assign DMX addresses to all the DMX functions contained in a fixture. 
     This will overwrite any existing addresses without warning. Multiple 
     registries or fixtures may be given for batch registration.

fixture_unaddress
^^^^^^^^^^^^^^^^^
Usage
     ``xA FIX``
Parameters
     *FIX* - the fixture to remove from all registries.
Synopsis
     Search through all registries and remove any links to DMX functions 
     that are children of a fixture.

fixture_remove
^^^^^^^^^^^^^^
Usage
     ``xr FIX``
Parameters
     *FIX* - the fixture to remove.
Synopsis
     Remove a fixture entirely from the effects plot. This does not remove 
     the fixture's functions from any DMX registries, so to purge the fixture 
     entirely, run fixture_unaddress first.
