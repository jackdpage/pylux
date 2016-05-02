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

Some commands call for an object as an argument. These are shown by capitalised 
arguments in the command description. This argument allows you to pipe 
in objects from the output of special listing commands. When a listing command 
is run, some lines on the output will be preceded by green integers, also 
called interface references. This 
shows that the object on that line can be piped into another command using 
that integer.

You can pipe in multiple objects at once. Pylux accepts comma-separated lists 
of integers, colon-separated ranges of integers and any combination of the two, 
for example ``1,4:9,11,20:28``.

For example, you may wish to set the gel colour of a specific fixture. First 
run the ``xl`` command to list all fixtures::
    1 SL spot (Hutton P650)
    2 SR spot (Hutton P650)
    3 White wash (Strand Coda 1000)
    4 Red wash (Strand Coda 1000)

Say you wanted to set the gel of the Red wash to Sunset Red, use the ``xs`` 
command, piping in object 4::
    xs 4 gel Sunset Red
