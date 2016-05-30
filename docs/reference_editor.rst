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


