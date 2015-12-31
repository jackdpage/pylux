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

    def get(self, ref):
        """Return the object of a user selection.

        Args:
            ref: the unique CLI identifier that the user selected.

        Returns:
            The object (which could be of any form) that is 
            associated with the reference in the option list.
        """
        try:
            ref = int(ref)
        finally:
            return self.option_list[ref]

    def clear(self):
        """Clear the option list."""
        self.option_list.clear()
        self.option_list['this'] = None


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
    i = 0
    parsed_input = []
    multiword_input = ""
    while i < number_args:
        parsed_input.append(inputs_list[i])
        i = i+1
    while number_args <= i <= len(inputs_list)-1:
        if multiword_input == "":
            multiword_input = multiword_input+inputs_list[i]
        else:
            multiword_input = multiword_input+' '+inputs_list[i]
        i = i+1
    parsed_input.append(multiword_input)
    return parsed_input
