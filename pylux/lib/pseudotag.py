'''The pseudotags lib file handles specific object tagging.

Often simple string tags are not enough or quick enough. Therefore 
certain tag keywords can be reserved such they invoke additional 
logic to parse the user input string, rather than just setting it as 
the value of the data tag.

For example, when the user uses the position tag, instead of setting 
the position tag to the given value, the program sets the posX and 
posY tags as given by the comma-separated coordinates in the value 
string.
'''

pseudotags = {}

# Tagging functions accept: obj, context, value:
#   obj: the object which is being edited
#   context: the context which is being used (contains the plot file and 
#            Interface object to allow pseudotags to access these attributes.
#   value: the unparsed value that the user entered.


def tag_position(obj, context, value):
    obj.data['posX'] = value.split(',')[0]
    obj.data['posY'] = value.split(',')[1]
    
def tag_focus(obj, context, value):
    obj.data['focusX'] = value.split(',')[0]
    obj.data['focusY'] = value.split(',')[1]

def tag_dimmer(obj, context, value):
    dimmer_function = context.interface.get('FIX', value)[0].uuid
    obj.data['controlDimmer'] = dimmer_function

def tag_name(obj, context, value):
    obj.name = value

pseudotags['position'] = tag_position
pseudotags['focus'] = tag_focus
pseudotags['dimmer'] = tag_dimmer
pseudotags['name'] = tag_name

