# Copyright 2015 Jack Page
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import xml.etree.ElementTree as ET
import uuid

projectFile = '../project/example.olp'

# Load the project file
tree = ET.parse(projectFile)
root = tree.getroot()

# Give the fixture that is to be created a UUID
fixtureUuid = str(uuid.uuid4())

# User specifies which OL fixture they are using
print('Currently adding a fixture to example.olp')
fixtureType = input('Enter the OLDoc ID of the fixture you are adding, followed by [ENTER]: \n')

print('Using fixture type '+fixtureType)

# Locate and parse the OLF file for this fixture type
treeFixtureSpec = ET.parse('../fixture/'+fixtureType+'.olf')
rootFixtureSpec = treeFixtureSpec.getroot()

# Find the variables for this fixture type
variables = rootFixtureSpec.find('variables')
# Create a dictionary to store the fixture details
details = {}
# Find the options and ask the user to specify them
for option in variables:
	optionValue = input('Choose a value for '+option.tag+' then press [ENTER]: \n')
	details[option.tag] = optionValue

# Find the constants and add them to a dictionary
constants = rootFixtureSpec.find('constants')
for option in constants:
	constantValue = option.tag
	details[option.tag] = option.text

# Confirm fixture options
print('Will now add a fixture of type '+fixtureType+' with these options')
print(details)

# Get the fixture list
fixtureList = root.find('fixtures')

# Create a new fixture
newFixture = ET.Element('fixture')
newFixture.set('olid', fixtureType) # Set OLID
newFixture.set('uuid', fixtureUuid) # Set UUID 
# Iterate over option values and add them to the new fixture
for i, j in list(details.items()): 
	newDetail = ET.SubElement(newFixture, i)
	newDetail.text = j

# Add the fixture to the fixture list
fixtureList.append(newFixture)
print('Added fixture with UUID '+fixtureUuid)

# Load the DMX registry
dmxRegistryXml = root.find('dmx_registry')	
dmxRegistryUuid = {} # Create fixture UUID dictionary
dmxRegistryFunction = {} # Create function dictionary
populatedAddresses = []

# Fill the dictionaries with the contents of the registry
for channel in dmxRegistryXml.findall('channel'):
	address = int(channel.get('address'))
	populatedAddresses.append(address)
	dmxRegistryUuid[address] = channel.find('fixture_uuid').text
	dmxRegistryFunction[address] = channel.find('function').text
print('The following DMX channels are populated in the registry:')
populatedAddresses.sort()
print(populatedAddresses)

# Load the DMX info for this fixture
dmxKeysXML = rootFixtureSpec.find('dmx_channels')
numberOfDmxKeys = 0
for dmxKey in dmxKeysXML:
	numberOfDmxKeys = numberOfDmxKeys + 1
print('The fixture you are adding requires '+str(numberOfDmxKeys)+' DMX channel(s)')

# Ask the user for the DMX start address
dmxStartAddress = input('Type the DMX start address for this fixture, followed by [ENTER]: \n')

# Append the DMX registry info
currentDmxAddress = int(dmxStartAddress)
for dmxKey in dmxKeysXML:
	newChannel = ET.Element('channel')
	newChannel.set('address', str(currentDmxAddress))
	newChannelUuid = ET.SubElement(newChannel, 'fixture_uuid')
	newChannelUuid.text = fixtureUuid
	newChannelFunction = ET.SubElement(newChannel, 'function')
	newChannelFunction.text = dmxKey.tag
	dmxRegistryXml.append(newChannel)
	print('Added new channel with address '+str(currentDmxAddress)+' and function '+dmxKey.tag)
	currentDmxAddress = currentDmxAddress + 1

tree.write(projectFile, encoding="UTF-8", xml_declaration=True)
