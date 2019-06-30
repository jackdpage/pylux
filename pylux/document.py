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


import decimal
import itertools
import json
import uuid


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


def get_by_ref(doc, type, ref):
    """Return an object of a given type and ref."""

    for obj in get_by_type(doc, type):
        if decimal.Decimal(obj['ref']).normalize() == decimal.Decimal(ref).normalize():
            return obj
    return False


def get_metadata(doc):
    '''Return all metadata objects.'''

    return get_by_type(doc, 'metadata')


def remove_by_uuid(doc, uuid):
    '''Remove an object with a matching UUID.'''

    doc.remove(get_by_uuid(doc, uuid))


def remove_by_ref(doc, type, ref):
    """Remove an object with a specific ref."""

    objs = get_by_type(doc, type)
    doc.remove(get_by_value(objs, 'ref', ref)[0])


def get_function_by_uuid(doc, uuid):
    '''Get a function by its UUID.'''

    for f in get_by_type(doc, 'fixture'):
        if 'personality' in f:
            for func in f['personality']:
                if func['uuid'] == uuid:
                    return func


def get_function_parent(doc, func):
    '''Get the associated fixture of a function.'''

    for f in get_by_type(doc, 'fixture'):
        if 'personality' in f:
            if func in f['personality']:
                return f


def get_occupied_addresses(reg):
    """Get a list of occupied addresses in a registry"""
    return sorted([int(d) for d in reg['table'].keys()])


def get_available_addresses(reg):
    """Get available addresses in a registry."""
    all = [i for i in range(1, 513)]
    occupied = get_occupied_addresses(reg)
    available = [i for i in all if i not in occupied]
    return sorted(available)


def get_start_address(reg, n):
    """Get start address in a registry given a required length."""
    available = get_available_addresses(reg)
    for addr in available:
        if set([i for i in range(addr, addr+n)]).issubset(available):
            return addr


def fill_missing_function_uuids(fix):
    """Add new UUIDs to the functions of a fixture where they are missing."""
    if 'personality' in fix:
        for func in fix['personality']:
            if 'uuid' not in func:
                func['uuid'] = str(uuid.uuid4())


def find_fixture_intens(fix):
    if 'personality' in fix:
        for func in fix['personality']:
            if func['name'] == 'Intens':
                return func


def get_function_patch_location(doc, func):
    """Finds a function in all registries and returns registry, address tuple."""
    locations = []
    for reg in get_by_type(doc, 'registry'):
        for d in reg['table']:
            if reg['table'][d] == func['uuid']:
                locations.append((reg['ref'], d))
    return locations


def autoref(doc, type):
    """Return an available reference number for a given type."""
    used_refs = []
    for obj in get_by_type(doc, type):
        used_refs.append(obj['ref'])

    for n in itertools.count(start=1):
        if n not in used_refs:
            return n