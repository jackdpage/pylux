CLI Features
============

The default interface used by Pylux is the CLI. The Pylux CLI acts very much 
like any other shell, but of course uses the Pylux command-set. To make 
navigating Pylux quicker, each command is a two-letter mnemonic (apart from 
some special utility commands) where the first letter represents the object 
which is going to have an action performed on it and the second letter 
represents the action to be performed. For example, ``ml`` is the mnemonic 
for listing all metadata.

Contexts
--------

In order to facilitate all the functionality of Pylux whilst still keeping 
the simple two letter mnemonics, and also to keep code cleaner, Pylux uses a 
system called contexts. A context is simply a set of commands that the user 
can access at any one time. The current context is indicated by the prompt, 
which will be of the form ``(pylux:CONTEXT)``. Commands for one context will 
not work in another context. For example, the aforementioned ``ml`` command 
is part of the ``editor`` context, so will not work in the ``plotter`` 
context.

Piping Complex Objects
----------------------

Some commands call for complex objects as input, for example, the ``xs`` 
command requires that you supply a Fixture object. This is, for obvious 
reasons, directly impossible with only a text prompt. For this reason, Pylux 
uses a system of on-screen references to allow you to pipe complex objects 
into commands.

Essentially, where the command calls for a complex object, you instead 
supply an integer or list of integers that correspond to the objects you wish 
to pass to the command. In order to generate such references, you will first 
need to run a listing or filtering command. The integer which represents 
each object is underlined. Every time you run a listing command, this set of 
references is refreshed, so be aware of what you are piping into commands if 
you have re-run a listing command.

In order to facilitate efficient processing of multiple objects at once, 
where a command allows for it, you may supply a comma-separated list of 
integers, such as ``2,8,10,22``. You can also specify ranges of sequential 
objects using a colon such as ``1:8``. You can, of course use any combination 
of these such as ``3,7:10,14,17:22``.

In addition to this, there is also a special reference, ``this`` which you can 
use in place of an integer list in order to use the same integers as you did 
for the previous command. If the reference list has changed, this will not 
necessarily supply the same objects, just the same integer references.

For example, you may wish to set the power of every PAR64 MFL to 1000W. First, 
you would use ``xf`` to display all such fixtures in the plot::

    xf type PAR64 MFL

This may give you an output such as (except the integers would be underlined)::

    1 PAR64 MFL, uuid: ...
    2 PAR64 MFL, uuid: ...
    3 PAR64 MFL, uuid: ...

Then you would use ``xs`` to set the power attribute to 1000, piping in all 
three fixtures::

    xs 1:3 power 1000

