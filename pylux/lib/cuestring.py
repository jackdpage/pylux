def get_action_string(action, document):
    if action.type.lower() == 'lx':
        output = document.get_object_by_uuid(action.output.uuid)
        s = '(LX) '+output.name
    elif action.type.lower() == 'sx':
        s = '(SX) '+action.output
    return s

def get_location_string(location, document):
    return '('+location.type.upper()+') '+location.event 
