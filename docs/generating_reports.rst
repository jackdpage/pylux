Generating Reports
==================

Pylux can generate all sorts of plaintext reports for display or printing. 
All reports are made using a Jinja 2 template. Jinja is a templating 
software that allows you to create any sort of plaintext template then 
populate it with the contents of the effects plot.

Pylux comes with some templates preinstalled but you can always place 
your own in ``~/.pylux/template``

Creating Reports
----------------

In order to create a report, you need to be in the ``reporter`` context, 
if you aren't already in it, switch to it::

    :reporter

To find out which templates are installed on your system run the template 
listing command::

    tl

This may give an output something like::

    0 hanglist (Pylux)
    1 fixturelist (Pylux)
    2 cuelist (Pylux)
    3 dimmers (System)
    4 custom (User)

Let's say you decide to generate the default fixture list; use the report 
generation command::

    rg 1

This generates your report and saves it internally. To get a list of all the 
internally saved reports, run::

    rl

Note that these reports are only saved for the current session and will be 
discarded as soon as you exit the ``reporter`` context. If you want to 
display the contents of the report on screen to check that it generated, 
you can run::

    rd 0

Saving Reports
--------------

Assuming everything is OK, you can now write your report to a file. Keep 
in mind that the path you supply is relative to the directory from which 
you launched Pylux::

    rw NewReport.html


