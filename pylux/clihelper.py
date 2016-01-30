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

 
class Interface:
    """Manage the CLI interactivity.

    Manage the interactive CLI lists, whereby a unique key which is 
    presented to the user on the CLI returns an object, without the 
    user having to specify the object itself.

    Attributes:
        option_list: a dictionary of the options presented to the 
            user on the CLI.
    """

    def __init__(self):
        """Create a dictionary for the options.

        Create a dictionary ready to populate with options, and add 
        an entry for the special 'this' with the value None.
        """
        self.option_list = {'this': None}

    def append(self, ref, object):
        """Add an object to the option list.

        Args:
            ref: the unique CLI identifier of the option being added.
            object: the object that should be returned if the user 
                selects this option.
        """
        self.option_list[ref] = object

    def get(self, refs):
        """Return the object of a user selection.

        Args:
            ref: the unique CLI identifier that the user selected.

        Returns:
            A list of objects that correspond to the references that 
            were given.
        """
        objects= []
        if refs == 'all':
            for ref in self.option_list:
                if ref != 'this':
                    objects.append(self.option_list[ref])
        else:
            if refs == 'this':
                refs = self.option_list['this']
            references = resolve_references(refs)
            for ref in references:
                objects.append(self.option_list[ref])
        return objects

    def clear(self):
        """Clear the option list."""
        self.option_list.clear()
        self.option_list['this'] = None

    def update_this(self, reference):
        """Update the 'this' special reference.

        Set the 'this' special reference to a specified reference. 
        If the given reference is also 'this', do nothing as 'this' 
        will already point to the desired reference.

        Args:
            reference: the reference that 'this' should point to.
        """
        if reference != 'this':
            self.option_list['this'] = reference


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


def get_fixture_print(fixture):
    """Return a string that represents this fixture the best.

    If the fixture has a name tag, return that, if not and it has a 
    type tag, return that, otherwise return the uuid.
    """
    if 'name' in fixture.data:
        return fixture.data['name']
    elif 'type' in fixture.data:
        return fixture.data['type']
    else:
        return fixture.uuid

