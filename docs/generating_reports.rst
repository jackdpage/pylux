Generating Reports
==================

Pylux can generate all sorts of plaintext reports for display or printing. 
All reports are made using a Jinja 2 template. Jinja is a templating 
software that allows you to create any sort of plaintext template then 
populate it with the contents of the effects plot.

Create a report from an existing template::

    Report Create fixturelist.html

This creates a report from the fixturelist.html template and stores it in
memory. Save it to disk by running::

    Report Write output.html

