class ObjectAlreadyExistsError(Exception):
    def __init__(self, obj_type, ref):
        super(ObjectAlreadyExistsError, self).__init__()
        self.obj_type = obj_type[1]
        self.ref = ref
