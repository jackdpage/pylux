def get_action_string(action, document):
    if cue.action.type.lower() == 'lx':
        output = document.get_object_by_uuid(cue.action.output.uuid)
        s = output.name
    elif cue.action.type.lower() == 'sx':
        s = cue.action.output
    return s

def get_location_string(location, document):
    return cue.location.event 
