Getting Started
===============

Invoking
--------

When Pylux is installed, it adds the ``pylux`` executable to your path, so 
you can launch Pylux by simply running ``pylux`` in a shell. Pylux also 
accepts some additional launch parameters.

-h  Print the usage message then exit.
-v  Print the version number then exit.
-g  Launch in GUI mode (non-functional).
-f FILE    Load FILE as the effects plot file.
-V  Set output verbosity. Include more than once for more verbosity.

For everyday use, you will probably only be using the -f parameter.

File Management
---------------

In addition to loading a file whlist launching Pylux, you can also load a 
file by issuing the ``fo path`` command when Pylux is open, which will 
discard the current file buffer and load the file at ``path``. When you need 
to save the file, run ``fw``.

If you do not have an existing file, you can begin working straight away. In 
order to save your file, you will have to specify a save location using the 
``fs path`` command, which sets the default save location for the currently 
loaded file to ``path``. After that you only need to run ``fw`` to save the 
file.

Note: Pylux does not have an autosaving feature so it is imperative that 
you run the ``fw`` command regularly.

Getting Help
------------

Pylux has some limited in-program help. Run the ``h`` command to display a 
list of commands available to you. You can then run ``h command`` to display 
specific help information on a certain command.

Contexts
--------

Contexts is a key feature of Pylux's CLI that allows command mnemonics to 
be kept to only two characters. A context can be thought of as a 'mode', 
where only a certain set of commands is available to you at any one time. 
For example, the ``reporter`` allows you to create plaintext documentation, 
but does not allow you to edit files. To edit files you must be in the 
``editor`` context.

You can always tell what context you are in by the prompt, which will be 
in the form ``(pylux:context)``.

In order to switch to a different context, run ``:context``.
