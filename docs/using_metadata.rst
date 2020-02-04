Using Metadata
==============

Metadata is a special form of data which exists outside of the normal object
structure. There are no references. It is simply a list of key/value pairs used
to store extra data about a file. There is only one command::

    Metadata Set title Romeo & Juliet

This gives the tag with key 'title' the value 'Romeo & Juliet'. If you want to delete
the tag, just run::

    Metadata Set title

That's it.
