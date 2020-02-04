Introduction
============

Synopsis
--------

Pylux is a program designed for the creation and management of documentation 
for entertainment purposes. Its primary purpose is the creation of 
documentation for theatrical lighting scenarios.

Pylux can be easily extended to encompass additional functionality and the 
default installation contains the necessary modules to create documentation 
in plaintext format of any style using simple templating tools.

Interface
---------

Everything you would need to do can be done through submitting commands on
the command line. In the current implementation, this is done through an
interactive prompt, although could be extended to incorporate a GUI, non-interactive
CLI or even a web interface.

Basic Concepts
--------------

Pylux is centered around a JSON file which contains all the information about 
your show. The JSON file is fundamentally unstructured and consists of an 
unordered list of fundamental objects, which will take one of the types below.

Fixture
    A single physical lighting fixture, such as a PAR can. A fixture will 
    further contain a list of DMX functions, which act in the same way as 
    the other fundamental objects, but will never appear outside of a fixture 
    object in the show file itself.

Registry
    A mapping of functions to addresses within a single DMX universe.

Cues
    A snapshot of the levels of some functions.

Groups
    A list of fixtures in a certain order.

These data types are referred to often in the remainder of this guide.

Each of these object types will have an arbitrary number of key/value pairs
associated with them. These pairs may contain any type of information, but
there are four which are common to all object types:

type
    The type of object. For example metadata or fixture.

uuid
    A universally unique identifier pointing to this object.

ref
    A human-readable identifier unique to this object within others of its
    type. This will be the number which is used to call and pass this object 
    to commands.

label
    A non-required field which acts as the fallback when no other information
    about the object is available.
