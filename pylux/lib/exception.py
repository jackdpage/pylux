class ObjectAlreadyExistsError(Exception):
    def __init__(self, obj_type, ref):
        super(ObjectAlreadyExistsError, self).__init__()
        self.obj_type = obj_type[1]
        self.ref = ref


class DependencyError(Exception):
    def __init__(self, missing_module):
        super(DependencyError, self).__init__()
        self.missing_module = missing_module


class ProgramExit(Exception):
    def __init__(self):
        super(ProgramExit, self).__init__()

