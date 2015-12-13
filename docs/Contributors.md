# pylux Documentation for Contributors

## Concepts

At its most basic level, pylux reads information from an XML file (the plot file) into Python objects, performs actions on those Python objects, then writes the changes back to the XML file. 
The OL Plot file contains all the information for a single lighting project. 
The plot file consists of three primary structures:

1. The metadata section: this section contains various elements containing information that applies to the entire document such as the venue, lighting designer, background image (for generating plot images) and scaling.

2. The fixtures list: this consists of multiple fixture elements, each of which is given a UUID. 
Each fixture has various child elements associated with it, depending on which type of OL Fixture it is (specified by its OLID).

3. The DMX registries: there can be multiple DMX registries in a plot file.
Each registry has a universe identifier associated with it.
The registry consists of multiple channel elements, each of which has an address attribute for the DMX512 address and children giving the UUID of the fixture the channel controls and its function.

## Classes

### The DmxRegistry class

The DmxRegistry class manages the reading, writing and editing of DMX registries in the plot file.

#### `__init__(universe)`

When the DmxRegistry class is initialised, it must be supplied with a `universe` variable.
This is the identifier that will be used for this registry both in the program and XML.
When the class is called for the first time, it will create an empty registry (a Python dictionary) as an object called `registry` create an object called `universe` containing the specified universe id.
It will then attempt to populate the Python dictionary by searching through the project file for a DMX registry with the same universe id. 
If it does find a registry in XML, it will populate the dictionary in the form `registry[address] = (fixture_uuid, function)`.
If it fails to find a registry in XML, it will create a new one with the specified universe id.

#### `save()`

When the save function is called, the program will iterate over the registry dictionary.
For each channel in the registry dictionary, it will check the project file to see if a channel with that address already exists in XML.
If the channel already exists, it will edit it with the parameters in the dictionary.
If the channel does not exist in XML, it will create a new one with the parameters and append it to the XML registry.

### The Fixture class

The fixture class is primarily used to add a fixture to the fixture list.

#### `__init__(olid)`

When the class is intialised, it must be supplied with an OpenLighting fixture id (olid).
The function then uses this olid to look up the data for the fixture by finding its XML file in the fixtures directory.
When the XML file for the fixture is found, two dictionaries are created, one for variables and one for constants, and their keys defined by the fixture XML files.
The values are left empty.
The dictionaries are available as the `variables` and `constants` objects respectively.
The function also creates a list of the functions of the DMX channels that the fixture uses.
This list is available as the `dmx` object.

#### `add()`

This function adds the fixture, in its current state, to the fixture list. 
If this function is called before the fixture values are defined using `edit()`, the fixture will be added to the fixture list with no values.
This will iterate over both variables and constants but will not manage the assignment of DMX channels.

##### `edit()`

This function is used to interactively set the values of the variables of the fixture.
In general, this function should be called before the `add()` function is called otherwise the variables will be left empty.
It will print out a prompt to the user asking them to specify a value for each variable in the dictionary.

### The FileManager class

This class is used to load, save and perform other functions on plot files.

#### `load(path)`

The load function will set the `file` object of FileManager to the path specified.
It will then get both the XML tree and root object from the file.

#### `save()`

The save function writes the current state of the XML tree to the file.
