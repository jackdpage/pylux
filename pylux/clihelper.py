# clihelper.py is part of Pylux
#
# Pylux is a program for the management of lighting documentation
# Copyright 2015 Jack Page
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

from pylux.lib import printer
from pylux import document
import decimal
from decimal import Decimal
import re


DECIMAL_PRECISION = decimal.Decimal('0.001')


def safe_resolve_dec_references_with_filters(doc, obj_type, user_input):
    """The safest most complete reference parser. Only return references of
    objects which exist in the document. Support for arbitrary decimal
    precision due to lookup nature of parsing. Support for filters across
    any range of inputs. Supports all keywords and symbols.
    Complete syntax:
    - comma separation for lists of ranges or single numbers
    - > symbol for ranges of numbers
    - future: ! symbol for removing a number or range of number
    - #[] for applying a filter to a range, single number, or any combination
      thereof. Where # is the number of the filter to apply.
    - * symbol for specifying all objects of the appropriate type.
    - * can also be used in filters e.g. 2[*],!2>4 is all objects of the
      given type that satisfy filter 2, and excluding objects 2 through 4
      (including all objects with decimal references in this range)"""

    obj_list = doc.get_by_type(obj_type)
    ranges = []
    points = []
    groups = []
    group_members = []
    catchalls = []
    calculated_refs = []
    # Matches filter ranges of the form #[range] where # is the filter ref
    # filtered_ranges is a list of tuples in the form (filter_ref, ranges)
    # for each filter range.
    filter_re = re.compile(r'(\d*\.?\d*)\[(.*?)\]')
    for fr in re.findall(filter_re, user_input):
        for r in fr[1].split(','):
            if '>' in r:
                ranges.append((fr[0], Decimal(r.split('>')[0]), Decimal(r.split('>')[1])))
            elif r == '*':
                catchalls.append(fr[0])
            elif '@' in r:
                groups.append((fr[0], decimal.Decimal(r.split('@')[1])))
            else:
                points.append((fr[0], decimal.Decimal(r)))
    # Remove all the filtered ranges from the input, and then search through
    # normally for the remainder
    for r in re.sub(filter_re, '', user_input).split(','):
        if '>' in r:
            ranges.append((0, decimal.Decimal(r.split('>')[0]), decimal.Decimal(r.split('>')[1])))
        elif r == '*':
            catchalls.append(0)
        elif '@' in r:
            groups.append((0, decimal.Decimal(r.split('@')[1])))
        else:
            try:
                points.append((0, decimal.Decimal(r)))
            except decimal.InvalidOperation:
                pass
    # Turn the groups into a list of fixture refs, but only if the type is fixture.
    # Filters applied to groups are also checked at this point.
    if obj_type is document.Fixture:
        for g in groups:
            if g[0]:
                filt = doc.get_by_ref(document.Filter, Decimal(g[0]))
            else:
                filt = None
            group = doc.get_by_ref(document.Group, Decimal(g[1]))
            for fix in group.fixtures:
                if filt:
                    try:
                        if fix.data[filt.key] == filt.value:
                            group_members.append(decimal.Decimal(fix.ref))
                    except KeyError or AttributeError:
                        pass
                else:
                    group_members.append(decimal.Decimal(fix.ref))
    # That's all the prep done, now check which of the objects in our all objects
    # list satisfies the ranges and points we've created.
    for obj in obj_list:
        ref = decimal.Decimal(obj.ref)
        if 0 in catchalls:
            calculated_refs.append(ref)
            continue
        elif len(catchalls):
            for i in catchalls:
                if i:
                    filt = doc.get_by_ref(document.Filter, Decimal(i))
                    try:
                        if obj.data[filt.key] == filt.value:
                            calculated_refs.append(ref)
                            continue
                    except KeyError or AttributeError:
                        pass
        if ref in group_members:
            calculated_refs.append(ref)
            continue
        for r in ranges:
            if r[0]:
                filt = doc.get_by_ref(document.Filter, Decimal(r[0]))
                try:
                    if r[1] <= ref <= r[2] and obj.data[filt.key] == filt.value:
                        calculated_refs.append(ref)
                        break
                except KeyError or AttributeError:
                    pass
            elif r[1] <= ref <= r[2]:
                calculated_refs.append(ref)
                break
        for p in points:
            if p[0]:
                filt = doc.get_by_ref(document.Filter, Decimal(p[0]))
                try:
                    if p[1] == ref and obj.data[filt.key] == filt.value:
                        calculated_refs.append(ref)
                        break
                except KeyError or AttributeError:
                    pass
            elif p[1] == ref:
                calculated_refs.append(ref)
                break

    return calculated_refs


def resolve_references(user_input, precision=1):
    """Parse the reference input.
    
    From a user input string of references, generate a list of 
    integers that can then be passed to the Interface class to 
    return objects. Parse comma separated values such as a,b,c 
    and greater-than sign separated ranges such as a>b, or a combination of
    the two such as a,b>c,d>e,f.
    """
    reference_list = []
    if len(user_input) > 0:
        all_input = user_input.split(',')
        for input_item in all_input:
            if '>' in input_item:
                limits = input_item.split('>')
                i = decimal.Decimal(limits[0])
                while i <= decimal.Decimal(limits[1]):
                    reference_list.append(i)
                    i += precision
            else:
                reference_list.append(decimal.Decimal(input_item))
        reference_list.sort()
    return reference_list


def resolve_dec_references(user_input):
    """Decimal version of the above."""
    return resolve_references(user_input, precision=DECIMAL_PRECISION)


def refsort(objs):
    """Sort a list of objects by their reference number"""
    return sorted(objs, key=lambda i: decimal.Decimal(i.ref))
