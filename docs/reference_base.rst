Base Reference
==============

Cue Commands
------------

Cue About
^^^^^^^^^
Usage
    ``Cue refs About``
Synopsis
    Show the intensities of all fixtures recorded in ``refs``.

Cue Create
^^^^^^^^^^
Usage
    ``Cue refs Create``
Synopsis
    Create empty cues at ``refs``.

Cue Display
^^^^^^^^^^^
Usage
    ``Cue refs Display``
Synopsis
    Show a single-line summary of ``refs``.

Cue Query
^^^^^^^^^
Usage
    ``Cue refs Query``
Synopsis
    Show the levels of all intensities and non-intensity parameters in ``refs``.

Cue Remove
^^^^^^^^^^
Usage
    ``Cue refs Remove``
Synopsis
    Remove ``refs`` from the show file entirely.

Cue Set
^^^^^^^
Usage
    ``Cue refs k v``
Synopsis
    Set arbitrary data tag ``k`` to ``v`` in ``refs``.

Cue SetIntens
^^^^^^^^^^^^^
Usage
    ``Cue refs SetIntens fixs level``
Synopsis
    Set the intensity of ``fixs`` to ``level`` in ``refs``.

File Commands
-------------

File Write
^^^^^^^^^^
Usage
    ``File Write path``
Synopsis
    Save the current working file to ``path``.

Filter Commands
---------------

Filter Create
^^^^^^^^^^^^^
Usage
    ``Filter refs Create k v``
Synopsis
    Create a filter at ``refs`` with requirement that arbitrary data tag ``k``
    has value ``v``.

Filter Remove
^^^^^^^^^^^^^
Usage
    ``Filter refs Remove``
Synopsis
    Remove ``refs`` from the show file entirely.

Fixture Commands
----------------

Fixture About
^^^^^^^^^^^^^
Usage
    ``Fixture refs About``
Synopsis
    Show all additional data tags and DMX functions of ``refs``.

Fixture Create
^^^^^^^^^^^^^^
Usage
    ``Fixture refs Create``
Synopsis
    Create empty fixtures at ``refs``.

Fixture CreateFrom
^^^^^^^^^^^^^^^^^^
Usage
     ``Fixture refs CreateFrom template``
Synopsis
    Create fixtures at ``refs``, using additional data tags and DMX functions
    from ``template``.

Fixture CompleteFrom
^^^^^^^^^^^^^^^^^^^^
Usage
     ``Fixture refs CompleteFrom template``
Synopsis
    For any additional data tags which exist in ``template`` but not ``refs``,
    copy the tag and value from ``template`` to ``ref``. Also copy the entire
    DMX personality if there is no personality in ``refs``.

Fixture CopyTo
^^^^^^^^^^^^^^
Usage
    ``Fixture ref CopyTo dests``
Synopsis
    Make a copy of ``ref`` at ``dests``.

Fixture Display
^^^^^^^^^^^^^^^
Usage
     ``Fixture refs Display``
Synopsis
    Show a single-line summary of ``refs``.

Fixture Patch
^^^^^^^^^^^^^
Usage
     ``Fixture refs Patch universe address``
Synopsis
    Patch ``refs``, beginning at ``address``, in ``universe``.

Fixture Remove
^^^^^^^^^^^^^^
Usage
     ``Fixture refs Remove``
Synopsis
    Remove ``refs`` entirely from the show file.

Fixture Set
^^^^^^^^^^^
Usage
     ``Fixture refs Set k v``
Synopsis
    Set arbitrary data tag ``k`` to ``v`` in ``refs``.

Fixture Unpatch
^^^^^^^^^^^^^^^
Usage
     ``Fixture refs Unpatch``
Synopsis
    Remove all entries in all universes of ``refs``.

Group Commands
--------------

Group About
^^^^^^^^^^^
Usage
    ``Group refs About``
Synopsis
    Show the constituent fixture references of ``refs``.

Group Append
^^^^^^^^^^^^
Usage
    ``Group refs Append fixs```
Synopsis
    Add fixtures ``fixs`` to the end of ``refs``.

Group Create
^^^^^^^^^^^^
Usage
    ``Group refs Create``
Synopsis
    Create empty groups at ``refs``.

Group Display
^^^^^^^^^^^^^
Usage
    ``Group refs Display``
Synopsis
    Show a single-line summary of ``refs``.

Group Query
^^^^^^^^^^^
Usage
    ``Group refs Query``
Synopsis
    Show a single-line summary of each fixture in ``refs``.

Group Remove
^^^^^^^^^^^^
Usage
    ``Group refs Remove``
Synopsis
    Remove ``refs`` entirely from the show file.

Group Set
^^^^^^^^^
Usage
    ``Group refs Set k v``
Synopsis
    Set arbitrary data tag ``k`` to ``v`` in ``refs``.

Metadata Commands
-----------------

Metadata Set
^^^^^^^^^^^^
Usage
    ``Metadata Set k v``
Synopsis
    Set the value of ``k`` to ``v``. Omit ``v`` to delete an existing
    entry under ``k``.

Registry Commands
-----------------

Registry About
^^^^^^^^^^^^^^
Usage
    ``Registry refs About``
Synopsis
    Show a table-style overview of used addresses in ``refs``.

Registry Create
^^^^^^^^^^^^^^^
Usage
    ``Registry refs Create``
Synopsis
    Create empty registries at ``refs``.

Registry Display
^^^^^^^^^^^^^^^^
Usage
    ``Registry refs Display``
Synopsis
    Show a single-line summary of ``refs``.

Registry Query
^^^^^^^^^^^^^^
Usage
    ``Registry refs Query``
Synopsis
    Show a single-line summary of every patched function in ``refs``.

Registry Remove
^^^^^^^^^^^^^^^
Usage
    ``Registry refs Remove``
Synopsis
    Remove ``refs`` entirely from the show file.