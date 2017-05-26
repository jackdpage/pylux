import os

LOCATIONS = {
        'home' : os.path.expanduser('~/.pylux'),
        'root' : os.path.abspath('/usr/share/pylux'),
        'devdir' : os.path.normpath(os.path.expanduser('~/Documents/GitHub/pylux/pylux/content'))}

# Priority of data locations, high to low
PRIORITY = ['devdir', 'home', 'root']

def get_data(path, location='auto'):
    # If location is auto, return the data from the directory with 
    # the highest priority. The general rule is the the closer to 
    # home the file is, the greater the priority
    path = os.path.normpath(path)
    if location == 'auto':
        for loc in PRIORITY:
            if os.path.isfile(os.path.join(LOCATIONS[loc], path)):
                return os.path.join(LOCATIONS[loc], path)
        return False
    elif location == 'all':
        paths = []
        for loc in PRIORITY:
            if os.path.isfile(os.path.join(LOCATIONS[loc], path)):
                paths.append(os.path.join(LOCATIONS[loc], path))
        return paths
    elif location in LOCATIONS:
        if os.path.isfile(os.path.join(LOCATIONS[location], path)):
            return os.path.join(LOCATIONS[location], path)
        else:
            return False
    else:
        return False

def list_data(path, location='all'):
    if location == 'all':
        files = []
        for loc in PRIORITY:
            if os.path.isdir(os.path.join(LOCATIONS[loc], path)):
                for data in os.listdir(os.path.join(LOCATIONS[loc], path)):
                    files.append(os.path.normpath(os.path.join(LOCATIONS[loc], path, data)))
        return files
    elif location in LOCATIONS:
        files = []
        if os.path.isdir(os.path.join(LOCATIONS[location], path)):
            for data in os.listdir(os.path.join(LOCATIONS[location], path)):
                files.append(os.path.abspath(data))
        return files
    else:
        return []
