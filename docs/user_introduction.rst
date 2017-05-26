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

Currently, Pylux's only interface is the command-line interface (CLI). 
Pylux uses an interactive prompt to accept commands from the user. A graphical 
user interface is not currently in development, although the infrastructure 
for one exists.

Basic Concepts
--------------

Pylux is centered around a file called an 'effects plot'. This file contains 
all the information necessary to produce additional documentation and run 
any queries. The effects plots rely on some fundamental data types which 
describe physical or abstract objects which Pylux interprets when it 
generates documentation. The fundamental data types are:

Fixture
    A single physical lighting fixture, such as a PAR can.

Registry
    A mapping of the functions of a single DMX512 universe.

Metadata
    Key/value strings that contain miscellaneous data, such as the director 
    of a production.

Cues
    A mapping between a location and an action. A location may be a point in 
    time or in a script. An action may be a lighting state or audio cue.

Scenes
    A snapshot of the state of the lighting output.

Chases
    Sequential scenes with additional data such as fade and dwell times.

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
    type.

name
    A non-required field which acts as the fallback when no other information
    about the object is available.
