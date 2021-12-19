Using Cues
==========

Cues work best when imported from an Eos ASCII export. There are no really useful
ways of constructing cues within the program. That's what a lighting desk is for.

Once you've imported a file, enter the Cue context by typing ``Cue Cue`` and
you will see all your cues, from all cue lists, in the fixed output pane.

You can use all the standard fixture commands on cues too, such as Display, Set,
About and Remove.

Cue Lists
---------

By default, any cue without an explicit cue list number is assumed to be in cue
list 1. Any cues not in cue list 1 will be displayed prefixed with the cue list
number and a slash. For example 2/101 is cue 101 in cue list 2. These are all
imported automatically with the Eos import.

When specifying cues on the command line, it is assumed that you are referring to
cues in cue list 1. Therefore ``Cue 1>100 Display`` will not show any cues in
other cue lists, even if their references are within range. To specify other cue
lists, use the prefix notation::

    Cue 2/1>100 Display

You don't need to use the prefix notation for the start and end of the range, the
program will know that you are referring to cue list 2. You will need to specify
the cue list for each range though::

    Cue 2/1>10,3/4,11/0> Display

This means cues 1 through 10 from cue list 2, cue 4 from cue list 3 and every cue
from cue list 11.

Showing Level Data
------------------

To see the level data of a cue, use the Query verb::

    Cue 1 Query

Any palettised data will, by default, be shown by its palette number, for example
``IP1`` or ``CP2``. This is the same behaviour as ETC Eos.

If you'd rather see the actual labels for the palettes, you can set the
``show-reference-labels`` option to True in the configuration. Alternatively,
you can set ``show-raw-data`` to True to show the actual numerical data stored
in the palette. In both these modes, colour coding will be retained so you can
easily see at a glance which data is palettised and which is absolute.

Values from previous cues in the same cue list will also track forward through cues
by default. The cue from which each level is tracking will display next to each
level in the list. This can be disabled by using the ``t`` flag.

By default, all non intensity parameters will be displayed. This can be disabled by
supplying the ``n`` flag. Flags can be combined together. For example, to query Cue 10
for intensity data only, and to ignore brought-forward tracked values::

    Cue 10 Query nt

Outputting Cues over sACN
-------------------------

You can output a snapshot of a cue over sACN. Currently only unicast is supported,
the settings for which can be changed in the configuration. To output cue 1::

    Cue 1 Output

Note that this output will be limited to levels which Eos defines in its cue
ASCII data. This is all intensity data and any non-intensity parameters which move
in the cue. Any tracked non-intensity parameters will not be displayed. Support
for tracking will come soon.

You should make sure you stop the output before exiting the program::

    Cue StopOutput

