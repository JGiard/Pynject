from pynject.builders import PynjectModelBuilder
from pynject.const import PYNJECT_ATTR, PYNJECT_MODEL, PYNJECT_SINGLETON


def pynject(cls):
    setattr(cls, PYNJECT_ATTR, True)
    model = PynjectModelBuilder(cls).build_model()
    setattr(cls, PYNJECT_MODEL, model)
    return cls


def singleton(cls):
    setattr(cls, PYNJECT_SINGLETON, True)
    return cls
