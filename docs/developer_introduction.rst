Developer Introduction
======================

This program is badly written.

The developer documentation here is purely so I don't forget how it works.

General Structure
-----------------

A front-facing *interface* sends raw commands to an *interpreter* and receives output via a message bus.

An interpreter may be extended through modules called extensions.

All document interaction takes place in ``document.py``.

