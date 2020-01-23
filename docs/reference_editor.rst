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
Synopsis
    List all the metadata objects in the effects plot file.

metadata_get
^^^^^^^^^^^^
Usage
    ``mg name``
Parameters
    *name* - the name to match against existing metadata.
Synopsis
    List all the metadata objects in the effects plot file whose name 
    matches *name*.

metadata_new
^^^^^^^^^^^^
Usage
    ``mn ref name``
Parameters
    *ref* - the reference number to assign to the new metadata, or ``auto``.
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
    ``mr ref``
Parameters
    *ref* - the item of metadata to remove from the effects plot.
Synopsis
    Completely remove an existing piece of metadata from the effects plot.

Fixture Commands
----------------

fixture_list
^^^^^^^^^^^^
Usage
    ``xl``
Synopsis
    List all existing fixtures in the file, printing their type and label 
    if present.

fixture_filter
^^^^^^^^^^^^^^
Usage
    ``xf tag value``
Parameters
    *tag* - the data tag of the fixtures to test.

    *value* - the value to match the fixture's data tags against.
Synopsis
    List all the fixtures in the effects plot who have a data tag called 
    *tag*, the value of which is equal to *value*.

fixture_get
^^^^^^^^^^^
Usage
     ``xg ref``
Parameters
     *ref* - the fixture to print the data tags of.
Synopsis
     List all the data tags associated with a fixture, including those 
     added automatically by Pylux.

fixture_getall
^^^^^^^^^^^^^^
Usage
     ``xG ref``
Parameters
     *ref* - the fixture to print the data tags and DMX functions of.
Synopsis
     List all the data tags associated with a fixture as per fixture_get, 
     but also list any DMX functions the fixture has associated with it.

fixture_new
^^^^^^^^^^^
Usage
     ``xn ref``
Parameters
     *ref* - The reference to give the new fixture, or ``auto``..
Synopsis
    Creates a new fixture from scratch. The fixture data tags, including 
    function list, will be completely empty.

fixture_from_template
^^^^^^^^^^^^^^^^^^^^^
Usage
     ``xN ref template``
Parameters
    *ref* - the refernce to give the new fixture, or ``auto``.
     *template* - the name of the template to load into this new fixture.
Synopsis
    Create a new fixture from an existing template file. All locations 
    specified in the data helper are searched. ``template`` will be of the 
    form Manufacturer/Model, and directories will be searched as such.

fixture_clone
^^^^^^^^^^^^^
Usage
     ``xc src dest``
Parameters
     *src* - the existing fixture to make a copy of.
     *dest* - the reference(s) of the new clone(s).
Synopsis
     Create a new fixture and populate its data dictionary and DMX functions 
     list with the contents of an existing fixture. New UUIDs are created so 
     the new fixture is not linked to the existing fixture.

fixture_set
^^^^^^^^^^^
Usage
     ``xs ref tag value``
Parameters
     *ref* - the fixture of which the data dictionary is to be changed.

     *tag* - the name of the tag to set the value of.

     *value* - the new value to assign to the tag.
Synopsis
     Set the value of a new or existing data tag in the fixture's data 
     dictionary. Tags must be one word, it is recommended to use 
     hyphenated-tags where more than one word is required, to maintain 
     consistency with standard Pylux tags.

fixture_address
^^^^^^^^^^^^^^^
Usage
     ``xa ref reg addr``
Parameters
     *ref* - the fixture who's functions are to be assigned addreses.

     *reg* - the registry to assign addresses in.

     *addr* - the address to begin registration at. Set to auto to allow 
               Pylux to choose the best start address.
Synopsis
     Assign DMX addresses to all the DMX functions contained in a fixture. 
     This will overwrite any existing addresses without warning. Multiple 
     registries or fixtures may be given for batch registration.

fixture_unaddress
^^^^^^^^^^^^^^^^^
Usage
     ``xA ref``
Parameters
     *ref* - the fixture to remove from all registries.
Synopsis
     Search through all registries and remove any links to DMX functions 
     that are children of a fixture.

fixture_remove
^^^^^^^^^^^^^^
Usage
     ``xr ref``
Parameters
     *ref* - the fixture to remove.
Synopsis
     Remove a fixture entirely from the effects plot. This does not remove 
     the fixture's functions from any DMX registries, so to purge the fixture 
     entirely, run fixture_unaddress first.

fixture_generate_autotags
~~~~~~~~~~~~~~~~~~~~~~~~~
Usage
    ``xS ref target``
Parameters
    *ref* - the fixture to generate tags for.
    *target* - (Optional) the type of tags to generate. Options are colour, 
        rotation and patch. Omit for all.
Synopsis
    Generates tags for a fixture based on existing tags and relationships.


fixture_complete_from_template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Usage 
    ``xct ref template``
Parameters
    *ref* - the fixture to update.
    *template* - the template to compare the fixture against.
Synopsis
    Compare a fixture with a specified template. If any tags exist in the 
    template and not the fixture, add them from the template. Do not 
    overwrite any existing tags in the fixture. Also does the same for 
    the fixture's function list.

