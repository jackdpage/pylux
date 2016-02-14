The Plot Module
===============

.. module:: plot

The plot module is the module in which you will find the majority of the 
functionality of Pylux. This module calls upon the ``xml.etree.ElementTree`` 
module to parse the XML files into Python-readable objects, then turns these 
into slightly nicer, more accessible objects that can be easily used by any 
other Pylux modules.

.. class:: PlotFile

    The PlotFile class deals with the loading and initial parsing of the plot 
    file. It defines some basic methods that are primarily used by the 
    ``editor`` context to perform standard file functions.


    .. attribute:: file

        :type: str

        The path of the plot file.

    .. attribute:: tree

        :type: ElementTree

        The tree of XML data as defined by the ``xml.etree.ElementTree`` 
        module. This is often referred to as the 'buffer' by this 
        documentation.

    .. attribute:: root

        :type: Element

        The root element (``plot``) of the XML tree.

    .. method:: load(path)

        Loads the file at the location with path ``path`` as the plot file. 
        Note you can only have a single plot file loaded at a time, so this 
        will discard the buffer of the previous file.

        :param str path:
            The path from which to load the plot file.

    .. method:: save()

        Saves the file buffer at the location given by the ``file`` attribute, 
        in other words saves the file to the location from which it was loaded.

    .. method:: saveas(path)

        Saves the file buffer at the location with path ``path``, where 
        ``path`` is a full system path.

        :param str path:
            The path to save the buffer to.

    .. method:: generate(path)

        Generate an empty plot file at the location with path ``path``. This 
        creates an empty document with only an XML declaration and root 
        ``plot`` element.

        :param str path:
            The path to save the empty plot file to.


.. class:: DmxRegistry

    The DmxRegistry class manages the DMX registries of the plot document. DMX 
    registries are lists of channels, which contain DMX addresses, and one or 
    more fixture UUID and function designators. Each DMX registry is uniquely 
    referenced by a user-defined universe identifier, as opposed to a randomly 
    generated UUID.

    .. attribute:: registry

        :type: dict

        The dictionary of registry information, in the form 
        ``{addr: [(uuid, func), ...], ...}``.

    .. attribute:: universe

        :type: str

        The name of the universe identifier of this registry.

    .. attribute:: xml_registry

        :type: Element

        For internal usage only. The registry in the XML tree.

    .. method:: __init__(plot_file, universe)

        :param PlotFile plot_file:
            The PlotFile object contaning the plot file.

        :param str universe:
            The universe identifier to be applied to this registry.

        Creates an empty registry with the universe identifier ``universe``. 
        Then searches for a registry in the XML tree with the same universe 
        identifier. If it finds a matching registry, loads the contents of 
        the XML registry into this registry object. If no matching registry 
        was found, creates a new empty registry in the XML tree.

    .. method:: save()

        Save the contents of the object to the XML tree. This should be called 
        every time the object is edited to preserve changes. This does not 
        write changes to the file.

    .. method:: get_occupied()

        :return: A list of occupied addresses.
        :rtype: list

        Get a list of the addresses of all the occupied channels in this 
        registry. 

    .. method:: get_start_address(n)

        :param int n:
            The number of DMX channels in a row that are required.
        :return: The best DMX start address to be used.
        :rtype: int

        Get a recommended start address for addressing all the channels of a 
        fixture. Searches in the registry for the next ``n`` free channels 
        in a row, and recommends this as a start address. If no channels are 
        occupied, reccomends 1.

    .. method:: add_function(address, fixture_uuid, function)``

        :param int address:
            The DMX address to add the function to.

        :param str fixture_uuid:
            The UUID of the fixture that is to be controlled by this channel.

        :param str function:
            The function of the fixture that this channel will control.

        Add a function to the channel with DMX address ``address``. Sets the 
        fixture UUID of this function to ``fixture_uuid`` and the name of this 
        function to ``function``.

    .. method:: remove_function(address, uuid)

        :param int address:
            The DMX address of the channel which the function is to be removed 
            from.

        :param str uuid:
            The UUID of the fixture that the function controls.

        Remove the function from the channel with DMX address ``address`` that 
        controls the fixture with UUID ``uuid``.

    .. method:: get_functions(address)

        :param int address:
            The DMX address of the channel to get the functions for.

        :return: 
            A list of fixture, function tuples controlled by this channel.
        :rtype: list

        Get a list of fixture, function tuples that are controlled by the 
        channel with the DMX address ``address``.

.. class:: RegistryList

    The RegistryList class is a very small class just in place to provide 
    access to all the registries in the plot file in an easy way.

    .. attribute:: registries

        :type: list

        A list of registry objects of all the registries in the XML tree.

    .. method:: __init__(plot_file)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        Searches through the plot file for any registries, creates DmxRegistry 
        objects for these and then appends them to the registries list.
