CLI Features
============

The default interface used by Pylux is the interactive command-line 
interface (CLI). From the prompt, Pylux accepts commands in the form 
``CMD arg1 arg2 ...``. All command names are a two character mnemonic where 
the first character represents the object and the second character the 
action to be performed on that object. The number and type of arguments 
vary greatly between commands.

Note that global commands are only a single character.


Contexts
--------

To facilitate the extending feature-set and for general code cleanliness, 
Pylux uses a system of 'contexts'. The user can only be in one context at any 
one time and only the commands provided by that context are available to the 
user at that time.

For example, in order to edit XPX files, you must be in the editor context. 
In order to generate reports you must be in the reporter context.

The current context is indicated by the prompt which will be of the form 
``(pylux:context)``. The default context can be set in the configuration but 
the default is editor.

The current context can be changed by issuing the ``:context`` command, where 
context is replaced by the name of the context to switch to.


Pipes
-----

On the CLI, you can only provide arguments in the form of strings. However, 
there are a number of other data forms that may be required by commands. For 
example, to set the value of a piece of metadata, you must provide the 
metadata object as an argument.

The passing of these objects into commands is facilitated by the piping 
system. The piping system relies on a special subset of commands: listing 
commands.

Listing Commands
^^^^^^^^^^^^^^^^

A listing command is any command which generates a list of objects of which 
the string representations are printed to the output. Along with the string 
representation of the object, listing commands also assign so-called 
interface references to each object. These are displayed as integers 
preceding the line which contains the object. It is these integers that are 
passed into commands in place of the objects they demand.

Pipe Syntax
^^^^^^^^^^^

Piped objects can simply be a single integer, `1`, a list of integers (in 
no particular order), `3,9,8,2`, a range of integers, `2:9`, or any 
combination of the above, `9,7,11:17,19`.

For example, in order to set the value of a piece of metadata, first run the 
metadata listing command, ``ml``, giving output::
    0   Director: J. Smith
    1   Designer: A. Wilson
    2   Master Electrician: P. Small

In order to change the name of the director, use the metadata setting 
command, ``ms``, piping in `0`::
    ms 0 T. Johnson

Documentation of Pipes
^^^^^^^^^^^^^^^^^^^^^^

Where a command calls for an object to be piped in, this will be made clear 
by the fact that the argument name will be in capitals, for example ``FIX``. 
There are a number of different object types that can be passed in, each of 
which is represented by a different colour on the CLI. They are:

======== ======
Arg Name Colour
======== ======
FIX      Green
FNC      Red
REG      Yellow
MET      Blue
CUE      NYI
======== ======
