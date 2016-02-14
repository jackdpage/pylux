Included Templates
==================

Pylux comes with a few Jinja templates for use with the ``reporter`` context. 
Jinja templates can be in any format and can be used to make extremely 
powerful output when written in HTML and combined with JavaScript 
interactivity. When specifying a template, you should not write the file 
extension. If there are multiple templates with the same name, Pylux will 
list them for you and let you choose.

Cue List
--------

Name
    cuelist

Formats
    HTML, TeX

Mandatory Arguments
    ``show``
        Which type of cues to show. Will only show cues whose ``type`` tag is 
        in this comma-separated list.

Optional Arguments
    ``style``
        (HTML only) The style kit to use. The default style kit is Milligram. 
        Pass ``style=bootstrap`` to use Twitter Bootstrap styling instead. 

Description
    A table of cues, showing cue identifier, location, description and notes.

Dimmer List
-----------

Name
    dimmerlist

Formats
    HTML, TeX

Description
    A list of fixtures showing fixture number and type, circuit, dimmer 
    channel and power, categorised by dimmer. Also displays sub totals for 
    dimmer power draw and total power draw.

Fixture List
------------

Name
    fixturelist

Formats
    HTML, TeX

Description
    A list of all fixtures in the plot, showing fixture number and type, power 
    and gel.

Hung Fixtures List
------------------

Name
    hanglist

Formats
    HTML, TeX

Description
    A list of all fixtures in the plot which have position values, showing 
    fixture type, position, focus coordinates, circuit and gel.
