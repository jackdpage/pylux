Using Cues
==========

Cues are essentially a link between two further objects: a cue action and 
a cue location. A cue action could be a lighting state change or a sound 
file. A cue location can be absolute (a single moment in time) or relative 
(a point in a script or relative to another cue).

Because cues are quite complicated compared to some other data types, an 
entire context exists to edit them. To get started, enter the ``qeditor`` 
context::

    :qeditor

Creating Actions
----------------

Let's start by adding a simple cue which maps a lighting scene to a moment 
in time (an absolute location). Start by creating the action::

    an lx 0 1,*,9

*0* is the reference to the scene we are connecting to the cue. *1,,9* is 
a comma-separated list of fade up, dwell and fade down times. This scene will 
fade up in one second, dwell for an unspecified period of time then fade down 
in nine seconds.

You will be able to see this action if you run the action listing command.

Let's create another action, but this time a sound cue. We will play a file 
on the filesystem::

    an sx file:///home/theatreuser/sound.ogg 3,100,3

This sound file will fade in for three seconds, play at 100% volume and then 
fade out for three seconds.

Creating Locations
------------------

Now for the location. We are using the absolute location definition system, 
which accepts the location as an ISO-8601 compliant date/time format. Our 
cue will fire on New Year's Day at midnight::

    ln abs 20170101T0000Z

Connecting Actions and Locations
--------------------------------

All that needs to be done now to create the cue is to connect the location 
and action with the cue creation command. Make sure you run the listing 
commands for both actions and locations first. Even though both cue actions 
are given in a single command, this command still creates two different cue 
objects::

    qn 0,1@0
