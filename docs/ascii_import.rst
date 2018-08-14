ASCII Import
============

There is limited support for importing show information in the USITT ASCII
format. Currently this is limited to conventional fixture patch. Advanced
patch and cue import is planned.

It is simple to import the conventional patch from a local file::

    ia show.asc patch

The keyword ``patch`` is required to tell Pylux to target the conventional
patch. Other import targets will become available as they are developed.

Pylux creates new fixtures for each fixture in the ASCII patch. It creates
these from a template as defined in the configuration file. By default this is
Generic/Dimmer. It will then address the fixtures in the DMX registries,
starting at registry 0. Currently, it will *not* create new registries. You
must create the registries it is going to populate before performing the
import.