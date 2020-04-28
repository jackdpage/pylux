Adding Object Types
===================

Adding object types is now substantially quicker due to new streamlined universal commands.

To create a new object type:

Add an object definition to ``lib.constant``, which will define the internal name for the object and the structure
of a blank such object in the file. Here should be defined any fields which are required for the object to work, for
example the ``levels`` field in a cue object.

Bootstrap off base commands in base. Available are create, display, remove and set. For each of these for your new
object, all you need is::

    def new_object_create(self, refs):
        return self._base_create(refs, constant.NEW_OBJECT_TYPE)

And then the same for display, remove and set.

You also need to register each of these commands by adding to ``register_commands``::

    self.commands.append(RegularCommand(('NewObject', 'Create'), self.new_object_create, check_refs=False))

The ``check_refs=False`` flag is only required for the create command.

Finally, add any other specialist commands to base and define any keymaps in the config file.