# OpenLighting Documentation

The OpenLighting Documentation (OLDoc) is a standard for the definition of XML lighting plots and fixtures. It also provides a reference software implementation written in Python.

## File Types

### Fixtures

Fixtures are defined by an OpenLighting Fixture file (extension .olf). This is an XML file with three components:
1. Constants definition - a list of specifications that do not change for this fixture
2. Variables definition - a list of specifications that may change dependent on usage
3. DMX address definition - a list of DMX addresses associated with the fixture, and their function

### Plots

Plots are defined by an OpenLighting Plot file (extension .olp). This is an XML file with three components:
1. Metadata - project data such as venue, background image, scaling, etc.
2. Fixtures - a list of fixtures and their locations in the plot. This is the entire fixture, with all its constants and variables included.
3. DMX registry - a list of DMX channels and their functions
