Importing Data
==============

You can import data from an Eos ASCII export::

  File ImportAscii export.asc eos_patch

This imports the Eos patch from the export.asc file. In place of ``eos_patch``, you
can also specify ``cues`` or ``groups``. Make sure you import the patch before
groups or cues, otherwise none of the fixtures you reference in these cues or groups
will exist yet.
