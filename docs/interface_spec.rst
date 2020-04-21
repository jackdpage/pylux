Interface Specification
=======================

The interface of the program is the point at which commands are issued to the interpreter, and the results and
outputs of commands relayed back to the end user. There is no requirement for how the interface itself operates, or
indeed how many of the potential features it incorporates. However, it must communicate with the interpreter in a
specific way.

For code-based reference, see ``cli.py`` which is the included interface. It should be relatively easy to understand
that file with the information in this page.

Launching
---------

The main process of the interface must be located in a function called ``main``, which has one argument. This
argument is the initialisation globals which are passed on launch of the program. These will contain the file to load,
parsed configuration, and potentially further globals in the future.

Structure
---------

Every interface must initialise an instance of ``interpreter.Interpreter``, to which it must pass on construction
the working show file, a message bus object, and the configuration file.

The working show file is the deserialised JSON document which has been parsed into a Python list. It is *not* the
load location of the file. The configuration file will have already been parsed into a dict when the main process
was launched, so this can safely be passed straight to the interpreter instance.

You must extend the interpreter manually with any extensions you wish to use, even the ``base`` extension. If you do
not add any extensions, the interpreter will not respond to any commands. To extend the interpreter, just pass the
string of the extension name to the ``register_extension`` function of your interpreter object.

Sending Commands
----------------

Commands are sent to the interpreter by sending the raw input string to the ``process_command`` function of your
interpreter instance. There is no need to process the string in anyway before sending it. If your interface relies on
the command line to perform interface-specific functions (for example, the CLI interface uses special unused commands
to change context), then you can process the command separately.

Receiving Feedback and Output
-----------------------------

Feedback (whether a command was successful or not) and output (data the command returns) are received through the
message bus object you passed to the interpreter instance on initialisation. This message bus object is a class
which must have two functions: ``post_feedback`` and ``post_output``. These are functions the interpreter will use
to communicate output back to your interface.

Both of these will receive text feedback in the format described below.

Format of Text Output
---------------------

As line breaks are very important in the interpretation of the data the interpreter returns, all text output is
returned as a list of lines, even if it is only one line long. Each of these lines (list items) could themselves be:

+ a string
+ a tuple
+ a list of strings and tuples

Any tuple returned will be of the form (FORMAT, STRING). This is to flag to your interface that there is specific
formatting to be added to STRING which will enhance its legibility. For example, it could be a colour to indicate
a specefic object type or status. The actual formatting to apply will not be specified, FORMAT is simply a string
indicating the *type* of formatting to add. For example ``fixture`` or ``function``. How you interpret these format
strings is entirely up to you. You may just
completely ignore them if you wish, although this could make the output more difficult for the end user to interpret.

A list of strings and tuples should be interpreted as a concatenation of the constituent strings.
