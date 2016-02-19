The RunSX Context
=================

The RunSX context is used to play back sound cues in the plot file by 
invoking mplayer. Therefore, in order to use RunSX, you will need mplayer 
installed on your system. Most package managers have mplayer available.

For a cue to be recognised by RunSX, it must have a ``file`` tag pointing to 
the sound file. The format can be anything which can be handled by mplayer.

You cannot edit sound cues in RunSX, they must be set up using the editor 
context before they can be used by RunSX.

In RunSX, cues can either be run individually, or they can be prepared as a 
stack, allowing the operator to simply provide the stack advance command to 
play the next cue.

Commands
--------

``ql``
    List all the sound cues which have associated sound files.

``qp CUE``
    Play the sound file associated with ``CUE``.
