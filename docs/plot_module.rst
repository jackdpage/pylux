The Plot Module
===============

The plot module is the module in which you will find the majority of the 
functionality of Pylux. This module calls upon the ``xml.etree.ElementTree`` 
module to parse the XML files into Python-readable objects, then turns these 
into slightly nicer, more accessible objects that can be easily used by any 
other Pylux modules.

The PlotFile Class
------------------

The PlotFile class deals with the loading and initial parsing of the plot 
file. It defines some basic methods that are primarily used by the ``editor`` 
context to perform standard file functions.

Attributes
^^^^^^^^^^

In general, these attributes should not be accessed outside of the class. 
They are available for use but wherever possible you should use one of the 
methods provided or another class.

``file``
    The path of the plot file.

``tree``
    The parsed XML tree, an object defined by ``xml.etree.ElementTree``. This 
    is often referred to as the buffer by this documentation.

``root``
    The root element (``plot``) of the XML tree.

Methods
^^^^^^^

``load(path)``
    Loads the file at the location with path ``path`` as the plot file. Note 
    you can only have a single plot file loaded at a time, so this will 
    discard the buffer of the previous file.

    **Arguments**

    ``path``
        The path from which to load the plot file.

``save()``
    Saves the file buffer at the location given by the ``file`` attribute, in 
    other words saves the file to the location from which it was loaded.

``saveas(path)``
    Saves the file buffer at the location with path ``path``, where ``path`` 
    is a full system path.

    **Arguments**

    ``path``
        The path to save the buffer to.

``generate(path)``
    Generate an empty plot file at the location with path ``path``. This 
    creates an empty document with only an XML declaration and root ``plot`` 
    element.

    **Arguments**

    ``path``
        The path to save the empty plot file to.


The DmxRegistry Class
---------------------

The DmxRegistry class manages the DMX registries of the plot document. DMX 
registries are lists of channels, which contain DMX addresses, and one or 
more fixture UUID and function designators. Each DMX registry is uniquely 
referenced by a user-defined universe identifier, as opposed to a randomly 
generated UUID.

Attributes
^^^^^^^^^^

``registry``
    The dictionary of registry information, in the form 
    ``{addr: [(uuid, func), ...], ...}``.

``universe``
    The name of the universe identifier of this registry.

``xml_registry``
    For internal usage only. The registry in the XML tree.

Methods
^^^^^^^

``__init__(plot_file, universe)``
    Creates an empty registry with the universe identifier ``universe``. Then 
    searches for a registry in the XML tree with the same universe identifier. 
    If it finds a matching registry, loads the contents of the XML registry 
    into this registry object. If no matching registry was found, creates 
    a new empty registry in the XML tree.

``save()``
    Save the contents of the object to the XML tree. This should be called 
    every time the object is edited to preserve changes. This does not write 
    changes to the file.

``get_occupied()``
    Get a list of the addresses of all the occupied channels in this registry. 

    **Returns**
    
    A list of integers representing the occupied addresses.

``get_start_address(n)``
    Get a recommended start address for addressing all the channels of a 
    fixture. Searches in the registry for the next ``n`` free channels in a 
    row, and recommends this as a start address. If no channels are occupied, 
    reccomends 1.

    **Arguments**

    ``n``
        The number of DMX channels required in a row.

    **Returns**

    An integer indicating the best start address.

``add_function(address, fixture_uuid, function)``
    Add a function to the channel with DMX address ``address``. Sets the 
    fixture UUID of this function to ``fixture_uuid`` and the name of this 
    function to ``function``.

    **Arguments**

    ``address``
        The DMX address to add the function to.

    ``fixture_uuid``
        The UUID of the fixture that is to be controlled by this channel.

    ``function``
        The function of the fixture that this channel will control.

``remove_function(address, uuid)``
    Remove the function from the channel with DMX address ``address`` that 
    controls the fixture with UUID ``uuid``.

    **Arguments**

    ``address``
        The DMX address of the channel which the function is to be removed 
        from.

    ``uuid``
        The UUID of the fixture that the function controls. This is to ensure 
        that in cases where one channel controls multiple fixtures, the 
        wrong fixture is not removed.

The RegistryList Class
----------------------

The RegistryList class is a very small class just in place to provide access 
to all the registries in the plot file in an easy way.

Attributes
^^^^^^^^^^

``registries``
    A list of registry objects of all the registries in the XML tree.

Methods
^^^^^^^

``__init__(plot_file)``
    Searches through the plot file for any registries, creates DmxRegistry 
    objects for these and then appends them to the registries list.
