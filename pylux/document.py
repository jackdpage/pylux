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


def write_to_file(doc, fp):
    '''Encode a document into a JSON file.'''

    with open(fp, 'w') as f:
        json.dump(doc, f)


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


def get_by_type(doc, type):
    '''Return objects of a given type.'''

    return get_by_value(doc, 'type', type)


def get_metadata(doc):
    '''Return all metadata objects.'''

    return get_by_type(doc, 'metadata')


def remove_by_uuid(doc, uuid):
    '''Remove an object with a matching UUID.'''

    doc.remove(get_by_uuid(doc, uuid))
