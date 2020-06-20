ERROR_MSG_OVERLAPPING_RANGE = 'Cannot copy one range to another. Provide a single source or destination start point only'
ERROR_MSG_EXISTING_OBJECT = '{0} {1} already exists. Will not overwrite existing object'
ERROR_MSG_UNIVERSE_SPACE = 'Insufficient space in universe {0}. Cannot patch fixture'
ERROR_MSG_UNPATCHED_FIXTURE = 'Fixture {0} has a value in {1} {2} but doesn\'t appear in the patch. It will be ignored'
ERROR_MSG_FAN_VALUES = 'Values could not be applied. Fan requires numeric start and end values'
ERROR_MSG_UNSUPPORTED_DATA = '{0} does not support arbitrary data tags'


class ObjectAlreadyExistsError(Exception):
    def __init__(self, obj_type, ref):
        super(ObjectAlreadyExistsError, self).__init__()
        self.obj_type = obj_type.noun
        self.ref = ref


class DependencyError(Exception):
    def __init__(self, missing_module):
        super(DependencyError, self).__init__()
        self.missing_module = missing_module


class ProgramExit(Exception):
    def __init__(self):
        super(ProgramExit, self).__init__()


class InsufficientAvailableChannels(Exception):
    def __init__(self, registry, n):
        super().__init__()
        self.registry = registry
        self.n = n
