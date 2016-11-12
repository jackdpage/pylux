# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
#
# Pylux is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylux is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import math


# File operations. These functions load JSON documents from files and
# deserialise into strings which can be used by object retrieval functions.

def get_string_from_file(fp):
	'''Load a file into a string.'''

	with open(fp, 'r') as f:
		s = f.read()

	return s


def get_deserialised_document_from_string(s):
	'''Deserialise a JSON document into a list.'''

	return json.loads(s)


# Object retrieval functions. These functions search a deserialised documents
# and return objects based on the given parameters.

def get_by_uuid(doc, uuid):
	'''Return object with given UUID.'''

	for obj in doc:
		if obj['uuid'] == uuid:
			return obj


def get_by_key(doc, k):
	'''Return objects which have a key in their dict.'''

	matched = []

	for obj in doc:
		if k in obj:
			matched.append(obj)

	return matched


def get_by_value(doc, k, v):
	'''Return objects which have a key matching a value.'''

	matched = []

	for obj in get_by_key(doc, k):
		if obj[k] == v:
			matched.append(obj)

	return matched


# Fixture processing functions. These functions take fixture objects as inputs,
# and calculate some value based on its parameters. They do not however edit
# the fixture objects themselves.

def get_fixture_rotation(fixture):
	'''Return the rotation of the fixture in the xy-plane.'''

	return math.atan2(fixture[pos][0], fixture[pos][1])


if __name__ == '__main__':
	print('You have executed Pylux without an interface. You\'re not going to '
		  'get far')
