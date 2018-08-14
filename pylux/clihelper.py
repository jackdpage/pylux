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


def print_object(obj, pre=''):
    s = printer.get_generic_string(obj, pre)
    print(s)


class Interface:
    '''Manage multiple buffers at a time.'''
    def __init__(self):
        self.buffers = {}
        self.entries = {}

    def add_buffer(self, s):
        self.buffers[s] = ReferenceBuffer()

    def get(self, buff, user_input):
        return self.buffers[buff].get(user_input)

    def open(self, buff):
        self.buffers[buff].begin()

    def add(self, s, obj, buff, pre=''):
        self.buffers[buff].append(obj, s, pre)


class ReferenceBuffer:
    '''Contains one set of interface references.

    The user can specify which reference buffer they wish to write 
    interface references to. (By default they are written to STD) 
    This allows multiple references to be accessed simultaneously.
    '''
    def __init__(self, colour=0):
        self.option_list = {}
        self.colour = colour

    def set_colour(self, colour):
        self.colour = colour
    
    def add(self, ref, obj):
        '''Add an object to the buffer.'''
        self.option_list[ref] = obj

    def get(self, refs):
        objs = []
        if refs == 'all':
            for ref, obj in self.option_list.items():
                objs.append(obj)
        else:
            for ref in resolve_references(refs):
                objs.append(self.option_list[ref])
        return objs

    def clear(self):
        '''Clear the reference buffer.'''
        self.option_list.clear()

    def begin(self):
        '''Start the buffer from empty.'''
        self.clear()

    def append(self, obj, s, pre):
        '''Append and print an object in the buffer.'''
        i = len(self.option_list)
        self.add(i, obj)
        print(pre+'\033[1m\033['+str(self.colour)+'m'+str(i)+'\033[0m '+s)
    
 
def resolve_references(user_input):
    """Parse the reference input.
    
    From a user input string of references, generate a list of 
    integers that can then be passed to the Interface class to 
    return objects. Parse comma separated values such as a,b,c 
    and colon separated ranges such as a:b, or a combination of 
    the two such as a,b:c,d:e,f.

    Args:
        user_input: the input string that the user entered.

    Returns:
        A list containing a list of integers.
    """
    reference_list = []
    if len(user_input) > 0:
        all_input = user_input.split(',')
        for input_item in all_input:
            if ':' in input_item:
                limits = input_item.split(':')
                i = int(limits[0])
                while i <= int(limits[1]):
                    reference_list.append(i)
                    i = i+1
            else:
                reference_list.append(int(input_item))
        reference_list.sort()
    return reference_list


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
    return sorted(objs, key=lambda i:i['ref'])