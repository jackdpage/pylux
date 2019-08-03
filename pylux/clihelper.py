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

from lib import printer
import document
import decimal


DECIMAL_PRECISION = decimal.Decimal('0.001')


def print_object(obj, pre=''):
    s = printer.get_generic_string(obj, pre)
    print(s)


def safe_resolve_dec_references(doc, type, user_input):
    """Parse decimal reference input.

    Takes the user input string as a list of comma-separated values, the values
    being either individual references or ranges of references represented by a
    colon. Resloves this collection of references into a list of valid
    string representations of decimals. Checks that each of these references
    actually represents an object in the show file, and returns the resulting
    list."""
    # Start with the complete possible range of reference numbers
    reference_list = resolve_dec_references(user_input)
    # Only return those who have an existing object
    return [i for i in reference_list if document.get_by_ref(doc, type, i)]


def resolve_references(user_input, precision=1):
    """Parse the reference input.
    
    From a user input string of references, generate a list of 
    integers that can then be passed to the Interface class to 
    return objects. Parse comma separated values such as a,b,c 
    and greater-than sign separated ranges such as a>b, or a combination of
    the two such as a,b>c,d>e,f.

    Args:
        user_input: the input string that the user entered.

    Returns:
        A list containing a list of integers.
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
    return [str(i) for i in reference_list]


def resolve_dec_references(user_input):
    """Decimal version of the above."""
    return resolve_references(user_input, precision=DECIMAL_PRECISION)


def resolve_input(inputs_list, number_args):
    """Parse user input that contains a multi-word argument.

    From a list of user arguments which have already been split, 
    return a new list containing a set number of arguments, where 
    the last argument is a multi-word argument is a multi-word
    argument.

    Args:
        inputs_list: a list containing strings which have been 
            split from the user input using split(' ').
        number_args: the number of arguments the input should 
            contain, excluding the action itself. For example, 
            the add metadata action takes two arguments: the tag 
            and value.

    Returns:
        A list containing a list of the arguments, where the last 
        argument is a concatenation of any arguments that were 
        left after processing the rest of the inputs list. For 
        example, the metadata example above would return 
        ['ma', 'tag', 'value which can be many words long'].
    """
    i = 1
    args_list = []
    multiword_input = ""
    while i < number_args:
        args_list.append(inputs_list[i])
        i = i+1
    while number_args <= i <= len(inputs_list)-1:
        if multiword_input == "":
            multiword_input = multiword_input+inputs_list[i]
        else:
            multiword_input = multiword_input+' '+inputs_list[i]
        i = i+1
    args_list.append(multiword_input)
    if args_list[-1] == '':
        args_list.pop(-1)
    return args_list


def refsort(objs):
    """Sort a list of objects by their reference number"""
    return sorted(objs, key=lambda i: decimal.Decimal(i['ref']))
