Getting Started
===============

Invoking
--------

Launch the program by running ``pylux`` as a module. Alternatively, you
can add an entry point into your system PATH.

-h  Print the usage message then exit
-v  Print the version number then exit
-f FILE    Load FILE as the current show file
-i INTERFACE    Use the specified interface in place of the default

File Management
---------------

Save the current working file at any time by running ``File Write``. You can also
change the default save location by running ``File WriteTo location``.

If you do not have an existing file, you can begin working straight away.
If no file is specified on startup, the program will load ``autosave.json``.

The CLI
-------

The CLI is the default and only included interface to the command interpreter.
It is a curses-style interface which will completely take over your terminal window.
The screen is split into four areas: a large pane on the left called the Fixed Output Pane,
a large pane on the right called the Dynamic Output Pane, a single line at the bottom
which is your command-line entry and a line above the command line which displays
command history and feedback.

The contents of the Dynamic Output Pane will change based on the commands you run and
will display any output the interpreter sends from commands.

The contents of the Fixed Output Pane are dependent on the context you are in. The
current context is given by the word preceding the command line. By default this is
Fixture. In the Fixture context, the Fixed Output Pane will display a list of all
fixtures in your show file. Similarly for cues, groups, etc. There is a special context,
All, which will display all items in your show file.

You can change the context by typing the name of the new context twice and pressing enter.
For example to change to the cue context type ``Cue Cue``. This is a function specific to
the CLI and is not sent to the interpreter so is not considered a 'command' as such.

You will notice as you type that many keys do not function as normal. That is because
there is a substantial autofill provision. For example, pressing the key ``x`` will
type ``Fixture`` in the command line for you, to save time typing out the entire word.
You can enable and disable autofill by pressing Ctrl+A. This will change the letter
preceding the command line from an A (indicating autofill is active) to an X.

Getting Help
------------

At any time you can type ``Program Help`` (shortcut *p* *h*) into the command line to
get a list of all available commands. Typing the name of a command after Program
Help will give you the usage for that specific command. For example
``Program Help Fixture Fan`` to get information about how to use the Fixture Fan
command.

Syntax
------

Most commands take the form ``object refs action params`` where:

- ``object`` is the type of object you will be acting on, for example Fixture.
- ``refs`` is a single or list of references to these objects, for example 1.
- ``action`` is what you are doing to this object, for example CopyTo.
- ``params`` is any further information the command requires. The number of parameters will vary from command to command. For example, CopyTo takes one parameter: the destination references.

References can be a single number::

    1

A range::

    1>10

Ranges can also be unbounded in either the min or max direction. Meaning
up to and including 100 and 100 and above respectively::

    >100
    >100
A list of numbers::

    1,8,11,15

Any combination of the two::

    1,3>10,13,15

A special character meaning all::

    *

A filtered list of numbers or ranges (this means apply filter 1 to the range in brackets)::

    1[2>8,10]

A combination of filtered and unfiltered ranges::

    1[2>8],11,12,2[22,26,29>40]

You can also apply a filter to the all character::

    1[*]

Filters can also be written inline::

    (fixture-type=Dimmer)[*]
    (label=Blackout)[1>100]

Or combine a filter of everything with unfiltered references too (this means show everything which
matches filter 1, and also show 8 and 9, regardless of whether they meet the requirements of filter 1
or not::

    1[*],8,9

When specifying fixtures, a reference can also be a group number::

    @30

Group numbers can be used alongside other components, including filters (this means show everything in group
30 that matches filter 1, 2 through 7 if they match filter 1, 9 regardless of whether it matches a filter,
and anything that matches filter 2)::

    1[@30,2>7],9,2[*]

When specifying cues, by default, only cues from cue list 1 will be shown. To access
other cue lists, specify it explicitly. Meaning cues 1 through 100 from cue list 2::

    2/1>100

Or all cues from cue list 7::

    7/0>
