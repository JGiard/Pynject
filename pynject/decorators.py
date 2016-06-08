from pynject.builders import PynjectModelBuilder
from pynject.const import PYNJECT_TYPEINFO, PYNJECT_ATTR, PYNJECT_MODEL


def listtype(param_name, param_sub_type):
    def class_decorator(cls):
        type_info = getattr(cls, PYNJECT_TYPEINFO, dict())
        type_info[param_name] = param_sub_type
        setattr(cls, PYNJECT_TYPEINFO, type_info)
        return cls

    return class_decorator


def pynject(cls):
    setattr(cls, PYNJECT_ATTR, True)
    model = PynjectModelBuilder(cls).build_model()
    setattr(cls, PYNJECT_MODEL, model)
    return cls
