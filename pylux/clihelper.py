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
from pylux.lib import exception
import decimal
from decimal import Decimal
import re
from collections import namedtuple


DECIMAL_PRECISION = decimal.Decimal('0.001')


# Tuple types for each of the fundamental types supported by the syntax
# filters is a list of filter objects to be applied to everything within
# that range/point/catchall
RefRange = namedtuple('RefRange', 'filters min max')
RefPoint = namedtuple('RefPoint', 'filters point')
RefCatch = namedtuple('RefCatch', 'filters')
RefGroup = namedtuple('RefGroup', 'filters group')


def _passes_filter(filt, obj):
    """Generic function for determining if an object satisfies a filter."""
    if filt is None:
        return True
    if str(obj.get(filt.key)) == str(filt.value):
        return True
    else:
        return False


def _passes_all_filters(filter_list, obj):
    if not filter_list:
        return True
    for i in filter_list:
        if not _passes_filter(i, obj):
            return False
    return True


def match_objects(user_input, doc=None, obj_type=None, precision=1):
    """Return a list of objects which satisfy the user_input conditions
    given. Supports all syntax.
    Complete syntax:
    - comma separation for conditions
    - > symbol for ranges of numbers
    - #[] for applying a filter to a list of conditions
    - * symbol for specifying all objects of the appropriate type.
    - * can also be used in filters e.g. 2[*],!2>4 is all objects of the
      given type that satisfy filter 2, and excluding objects 2 through 4
      (including all objects with decimal references in this range)
    - @ to specify a group
    - #/ to indicate cue list # (default cue list 1)"""
    if not doc or not obj_type:
        return resolve_references(user_input, precision=precision)

    obj_list = doc.get_by_type(obj_type)
    conditions = []

    def _resolve_condition(condition_string):
        """Resolve a condition string into one of the above four key types.
        Note that this is just the string for the condition, and not the filter
        part, if applicable. However, this function can still add filters in the
        form of cue list filters.
        Accepts a comma-separated condition list as condition_string"""
        _conditions = []
        for condition in condition_string.split(','):
            if '>' in condition:
                r_min = condition.split('>')[0]
                r_max = condition.split('>')[1]
                if '/' in r_min and obj_type is not document.Cue:
                    raise exception.ReferenceSyntaxError('Slash symbol should be used for cue identifiers only')
                # If the / symbol is the min value, we take that as the cue list to
                # use and create a new filter for that. If the / symbol is also in the
                # max value, we need to check that it has specified the same cue list
                # as we cannot return a range across cue lists. If there is not / symbol
                # in the max value, assume that the max is using the same cue list
                # as the min. If no cue list number has been provided through the slash
                # syntax, we assume cue list 1 and make a filter for that instead.
                if '/' in r_min and obj_type is document.Cue:
                    cue_list_filter = document.Filter(key='cue_list', value=r_min.split('/')[0])
                    r_min = r_min.split('/')[1]
                    if '/' in r_max:
                        if r_max.split('/')[0] != r_min.split('/')[0]:
                            raise exception.ReferenceSyntaxError('Cannot specify a range spanning multiple cue lists')
                        r_max = r_max.split('/')[1]
                elif obj_type is document.Cue:
                    cue_list_filter = document.Filter(key='cue_list', value='1')
                else:
                    cue_list_filter = None
                try:
                    r_min = decimal.Decimal(r_min)
                except decimal.InvalidOperation:
                    raise exception.ReferenceSyntaxError('Could not convert ' + r_min + ' to decimal')
                try:
                    r_max = decimal.Decimal(r_max)
                except decimal.InvalidOperation:
                    raise exception.ReferenceSyntaxError('Could not convert ' + r_max + ' to decimal')
                _conditions.append(RefRange([cue_list_filter], r_min, r_max))
            elif condition == '*':
                _conditions.append(RefCatch([]))
            # If the object type isn't Fixture, groups cannot be used. Instead
            # of throwing a syntax error, we will just quietly ignore them
            # and carry on.
            elif '@' in condition and obj_type is document.Fixture:
                group = doc.get_by_ref(document.Group, decimal.Decimal(condition.split('@')[1]))
                _conditions.append(RefGroup([], group))
            else:
                if '/' in condition and obj_type is document.Cue:
                    cue_list_filter = document.Filter(key='cue_list', value=Decimal(condition.split('/')[0]))
                    condition = condition.split('/')[1]
                elif obj_type is document.Cue:
                    cue_list_filter = document.Filter(key='cue_list', value='1')
                else:
                    cue_list_filter = None
                try:
                    condition = decimal.Decimal(condition)
                except decimal.InvalidOperation:
                    raise exception.ReferenceSyntaxError('Could not convert '+condition+' to decimal')
                _conditions.append(RefPoint([cue_list_filter], condition))
        return _conditions

    # Matches filter ranges of the form #[range] where # is the filter ref
    # filtered_ranges is a list of tuples in the form (filter_ref, ranges)
    # for each filter range. The regex provides two groups: the first being
    # the reference of the filter and the second being the conditions the
    # filter is being applied to.
    filter_re = re.compile(r'(\d*\.?\d*)\[(.*?)\]')
    for fr in re.findall(filter_re, user_input):
        filter_obj = doc.get_by_ref(document.Filter, Decimal(fr[0]))
        if not filter_obj:
            raise exception.ReferenceSyntaxError('Could not find filter '+fr[0])
        for c in _resolve_condition(fr[1]):
            c.filters.append(filter_obj)
            conditions.append(c)

    # Remove all the filtered ranges from the input, and then search through
    # normally for the remainder
    for c in _resolve_condition(re.sub(filter_re, '', user_input)):
        conditions.append(c)

    # Now we have all the conditions neatly organised in a list, we just
    # iterate over the object list we got earlier and check which objects
    # match one of the specified conditions.

    # First of all, if there's a catchall with no filter, we can just return
    # the entire object list straight away and not bother with any of this.
    if RefCatch([]) in conditions:
        return obj_list

    def _is_match(test):
        """Checks an object against all conditions and returns True if it
        matches any of them."""
        ref = Decimal(test.ref)
        for c in [x for x in conditions if type(x) == RefCatch]:
            if _passes_all_filters(c.filters, test):
                return True
        for c in [x for x in conditions if type(x) == RefPoint]:
            if _passes_all_filters(c.filters, test) and ref == c.point:
                return True
        for c in [x for x in conditions if type(x) == RefRange]:
            if _passes_all_filters(c.filters, test) and c.min <= ref <= c.max:
                return True
        for c in [x for x in conditions if type(x) == RefGroup]:
            if _passes_all_filters(c.filters, test) and test in c.group.fixtures:
                return True
        return False

    matched = []
    for obj in obj_list:
        if _is_match(obj):
            matched.append(obj)

    return matched


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
