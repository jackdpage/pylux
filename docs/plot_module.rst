The Plot Module
===============

.. module:: plot

The plot module is the module in which you will find the majority of the 
functionality of Pylux. This module calls upon the ``xml.etree.ElementTree`` 
module to parse the XML files into Python-readable objects, then turns these 
into slightly nicer, more accessible objects that can be easily used by any 
other Pylux modules.

.. class:: PlotFile

    The PlotFile class deals with the loading, generation and initial parsing 
    of plot files, the fundamental component of the Pylux system.

    **Public Methods**

    .. method:: __init__(path=None)

        :param str path:
            If a file is to be loaded on initialisation, the full system path 
            from which to load it.

        :raises FileNotFoundError:
            If no file exists at ``path`` in the filesystem.

        :raises FileFormatError:
            If the XML parser raises :exc:`~xml.etree.ElementTree.ParseError`.

        Prepares the PlotFile instance for a file to be loaded. If the ``path`` 
        parameter is given, attempts to load and parse the XML file at that 
        path using the :meth:`load` method.

        If the ``path`` parameter is not given or is ``None``, will create a 
        new plot file using the :meth:`new` method.

    .. method:: load(path)

        :param str path:
            The full system path from which to load the plot file.

        :raises FileNotFoundError:
            If no file exists at ``path`` in the filesystem.

        :raises FileFormatError:
            If the XML parser raises :exc:`~xml.etree.ElementTree.ParseError`.

        Load the file at ``path`` into the object, and attempt to parse it 
        into an XML tree.

    .. method:: new()

        Create an empty :class:`~xml.etree.ElementTree.ElementTree` in 
        :attr:`tree`, overwriting any existing tree, and set the 
        root of this tree and :attr:`root` to a new ``plot`` element.

    .. method:: write()

        Write the contents of :attr:`tree` to the location defined by 
        :attr:`path`, in UTF-8 encoding and with an XML declaration.

    .. method:: write_to(path)

        :param str path:
            The full system path to save the tree to.

        Write the contents of :attr:`tree` to ``path``. This does not change 
        :attr:`path`.

    **Public Attributes**

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

.. class:: DmxRegistry

    The DmxRegistry class manages the DMX registries of the plot document. DMX 
    registries are lists of channels, which contain DMX addresses, and one or 
    more fixture UUID and function designators. Each DMX registry is uniquely 
    referenced by a user-defined universe identifier, as opposed to a randomly 
    generated UUID.

    **Public Methods**

    .. method:: __init__(plot_file, universe)

        :param PlotFile plot_file:
            The PlotFile object contaning the plot file.

        :param str universe:
            The universe identifier to be applied to this registry.

        Create an empty registry with the universe identifier ``universe``. 
        Then searche for a registry in the XML tree with the same universe 
        identifier. If a matching registry is found, load the contents of 
        the XML registry into this registry object. If no matching registry 
        was found, create a new empty registry in the XML tree.

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

    .. method:: add_function(address, fixture_uuid, function)

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

    **Private Methods**

    .. method:: _save()

        Save the contents of the object to the XML tree. This should be called 
        every time the object is edited to preserve changes. This does not 
        write changes to the file.

    **Public Attributes**

    .. attribute:: registry

        :type: dict

        The dictionary of registry information, in the form 
        ``{addr: [(uuid, func), ...], ...}``.

    .. attribute:: universe

        :type: str

        The name of the universe identifier of this registry.

    **Private Attributes**

    .. attribute:: _xml_registry

        :type: Element

        The ElementTree object containing the XML registry.

.. class:: RegistryList

    The RegistryList class is a very small class just in place to provide 
    access to all the registries in the plot file in an easy way.

    **Public Methods**

    .. method:: __init__(plot_file)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        Searche through the plot file for any registries, create DmxRegistry 
        objects for these and then append them to the registries list.

    **Public Attributes**

    .. attribute:: registries

        :type: list

        A list of registry objects of all the registries in the XML tree.

.. class:: Fixture

    The Fixture class manages individual fixtures in the plot. Fixtures are 
    the most fundamental component of the plot file and contain a significant 
    amount of data that is accessed by output functions.

    **Public Methods**

    .. method:: __init__(plot_file, uuid=None, template=None, src_fixture=None)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        :param str uuid:
            The UUID of the fixture to load into this object.

        :param str template:
            The full system path of the fixture template file to load 
            information from.

        :param Fixture src_fixture:
            The :class:`Fixture` object to clone the data from into this 
            fixture object.

        Create a fixture object then populate it with data in one of three 
        ways: provide a UUID to search the plot file then populate with the 
        data found in the corresponding fixture in XML; provide a template 
        file to load the data from the template file into this fixture; or 
        provide a source Fixture object to copy the data from that fixture 
        into this one.

        If more than one of these three paramaters is given, priority is 
        given as such: ``uuid > template > src_fixture``. If none of the 
        three are given, the Fixture object remains empty.

    .. method:: set_data(name, value)

        :param str name:
            The name of the data to set.

        :param str value:
            The new value of the data.

        Set the value of a piece of fixture data then save the edited fixture 
        to the XML tree. This should be used in favour of directly editing 
        the contents of the data dictionary as directly editing the dictionary 
        does not save the contents to the tree so the changes are not 
        permanent.

    .. method:: get_data(name)

        :param str name:
            The name of the data to be returned.

        :return: The value of the data.
        :rtype: str

        Get the value of a piece of a fixture's data with name ``name``. 
        This is essentially just a wrapper around the data dictionary. The 
        same result could be achieved using::

            self.data[name]

    .. method:: address(registry, start_address)

        :param Registry registry:
            The registry to address this fixture in.

        :param int start_address:
            The DMX address at which to start the fixture addressing.

        Assign consecutive DMX addresses for all the channels required by 
        this fixture. Starting at ``start_address``, assigns DMX functions in 
        ``registry`` for all the functions listed in the ``dmx_functions`` 
        data tag.

    .. method:: unadress(registries)

        :param RegistryList registries:
            The :class:`RegistryList` object containing all the DMX registries 
            in the plot.

        Remove, from every registry, any function that is connected to the 
        UUID of this fixture.

    .. method:: get_rotation()

        :return: The rotation angle in degrees.
        :rtype: float

        Based on the position and focus data for the fixture, return the 
        angle, in degrees, which the axis of this fixture makes with the 
        positive y-axis. Return ``None`` if the rotation cannot be 
        calculated.

    .. method:: get_colour()

        :return: The hexadecimal colour code for the fixture.
        :rtype: str

        Based on the gel data for this fixture and the gel colours reference, 
        return the hexadecimal colour code of the gel for this fixture. 
        Return ``None`` if there is no gel data or the gel name does not 
        appear in the reference dictionary.

    **Private Methods**

    .. method:: _new_from_template(template_file)

        :param str template_file: 
            The full system path of the template file to load data from.

        Create a new random UUID for this fixture, then populate its data 
        dictionary with the contents of the template file.

    .. method:: _new_from_fixture(src_fixture)

        :param Fixture src_fixture:
            The :class:`Fixture` object from which to load data.

        Create a new random UUID for this fixture, then populate its data 
        dictionary with the contents of the source fixture's data dictionary.

    .. method:: _save()

        Save the fixture data dictionary to the XML tree.

    **Public Attributes**

    .. attribute:: uuid

        :type: str

        The UUID of the fixture in string form.

    .. attribute:: data

        :type: dict

        A dictionary containing all the basic data of the fixture. i.e. 
        information which can be represented as a single string.

    **Private Attributes**

    .. attribute:: _xml_fixture

        :type: Element

        The :class:`~xml.etree.ElementTree.Element` in the XML tree 
        containing the information about this fixture.

.. class:: FixtureList

    The FixtureList class manages and performs functions which require 
    knowledge of all fixtures. For example, the removal of fixtures and the 
    assignment of data that is dependent on the existence of other fixtures.

    **Public Methods**

    .. method:: __init__(plot_file)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        Create :class:`Fixture` objects for every fixture in the plot file, 
        and add them to an accessible list.

    .. method:: remove(fixture)

        :param Fixture fixture:
            The fixture to be removed.

        Remove a fixture from the plot. Note this does not unaddress the 
        fixture, use :meth:`Fixture.unaddress` for that.

    .. method:: get_data_values(data_type)

        :param str data_type:
            The data name to search for in fixture data dictionaries.
        :return: A list of all the values used for ``data_type``.
        :rtype: list

        Return a list containing all the values used for data with the name 
        ``data_type`` by any fixture in the plot.

    .. method:: assign_usitt_numbers()

        Doesn't really assign USITT numbers but close enough. Sets the value 
        of the ``usitt_key`` data tag for each fixture such that the fixtures 
        are numbered in ascending order of their ``posY`` value. If the 
        fixture doesn't have ``posY`` in its data dictionary, the USITT key is 
        given the value ``None``.

    .. method:: get_fixtures_for_dimmer(dimmer)

        :param Fixture dimmer:
            The fixture to find the controlled fixtures for. (Presumably a 
            dimmer).
        :return: A list of Fixture objects controlled by this fixture.
        :rtype: list

        If ``dimmer`` is a dimmer, search through the fixture list to find 
        fixtures which have this dimmer's UUID in their ``dimmer_uuid`` tag. 
        Return a list of all such found fixtures.

        If ``dimmer`` turns out not to be a dimmer, return an empty list.

    **Public Attributes**

    .. attribute:: fixtures

        :type: list

        A list of :class:`Fixture` objects giving every fixture in the plot 
        file.

    **Private Attributes**

    .. attribute:: _root

        :type: Element

        The root of the plot file. Equivalent to :attr:`PlotFile.root`.

.. class:: Metadata

    The Metadata class manages all the metadata in the plot. As metadata is 
    simply in the form tag=value, there is no need to have a separate object 
    for each piece of metadat.

    **Public Methods**

    .. method:: __init__(plot_file)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        Search through the XML tree for all metadata and load into the 
        metadata dictionary.

    .. method:: set_data(name, value)

        :param str name:
            The name of the metadata to be set.

        :param str value:
            The new value to set the metadata to.

        Set the value of a piece of metadata and save to the XML tree. This 
        is preferred over directly editing the metadata dictionary as the 
        latter does not save the result to XML and therefore any changes are 
        only temporary.

    .. method:: get_data(name)

        :param str name:
            The name of the metadata whose value should be returned.
        :return: The value of the metadata.
        :rtype: str

        Return the value of a piece of metadata. If the metadata does not 
        exist in the dictionary, return ``None``. This is equivalent to::

            self.meta[name]

    **Private Methods**

    .. method:: _save()

        Save the contents of the metadata dictionary to the XML tree, creating 
        new elements where appropriate.

    **Public Attributes**

    .. attribute:: meta

        :type: dict

        A dictionary containing all the metadata in the plot file.

    **Private Attributes**

    .. attribute:: _root

        :type: Element

        The root of the plot file. Equivalent to :attr:`PlotFile.root`.

.. class:: Cue

    The Cue class manages a single cue in the plot file at a time, and its 
    associated data.

    **Public Methods**

    .. method:: __init__(plot_file, UUID=None)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        :param str uuid:
            The UUID of the cue to be loaded.

        Create a new cue object. If a UUID is given, search for it in the 
        XML tree then load data from XML if it is found.

        If no UUID is given, create a new cue in XML, with a new random 
        UUID and a sorting key one greater than the current sorting key.

    .. method:: set_data(name, value)

        :param str name: The name of the data to set.
        :param str value: The new value of the data to be set.

        Set the value of the data ``name`` to ``value``. Preferred over 
        directly editing the data dictionary as it also saves to XML, making 
        changes permanent.

    .. method:: get_data(name)

        :param str name: The name of the data to be returned.
        :return: The value of ``name``.
        :rtype: str

        Return the value of the data tag ``name``. If ``name`` is not in the 
        cue's data dictionary, return ``None``.

    **Private Methods**

    .. method:: _save()

        Save the contents of the cue's data dictionary, and its current 
        sorting key, to the XML tree.

    **Public Attributes**

    .. attribute:: uuid

        :type: str

        The UUID of the cue in string form.

    .. attribute:: key

        :type: int

        The sorting key of the cue. This is the number which determines at 
        which point, relative to the other cues in the cue list, this cue 
        occurs.

    .. attribute:: data

        :type: dict

        A dictionary of all the other data associated with the cue.

    **Private Attributes**

    .. attribute:: _xml_cue

        :type: Element

        The :class:`~xml.etree.ElementTree.Element` in the XMl tree 
        containing the information about this cue.

.. class:: CueList

    The CueList class performs functions on cues that can only be performed 
    with knowledge of the state of all other cues.

    **Public Methods**

    .. method:: __init__(plot_file)

        :param PlotFile plot_file:
            The PlotFile object containing the plot file.

        Create a list of all the cues in the plot file in an accessible 
        attribute.

    .. method:: remove(cue)

        :param Cue cue: The cue to remove from the plot.

        Remove a cue from the plot entirely.

    .. method:: move_after(origin, dest)

        :param int origin: The sort key of the cue to be moved.
        :param int dest: The sort key of the cue which should come immediately 
            before this cue after the move.

        Adjust the sort keys of any necessary cues such that ``origin`` comes 
        directly after ``dest`` in the sort order.

    .. method:: move_before(origin, dest)

        :param int origin: The sort key of the cue to be moved.
        :param int dest: The sort key of the cue which should come immediately 
            after this cue after the move.

        Adjust the sort keys of any necessary cues such that ``origin`` comes
        directly before ``dest`` in the sort order.

    .. method:: assign_identifiers()

        Set the ``identifier`` tags in the cue data dictionaries of all cues 
        such that each cue has an identifier which is its type followed by a 
        number determined by its sort order. Each type has its own counter, so 
        the number following the type will not necessarily be the same as the 
        cue's sort key.

    **Public Attributes**

    .. attribute:: cues

        :type: list

        A list of :class:`Cue` objects of all the cues in the plot file.

    **Private Attributes**

    .. attribute:: _root

        :type: Element

        The root of the plot file. Equivalent to :attr:`PlotFile.root`.
