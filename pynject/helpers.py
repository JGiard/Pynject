from inspect import signature, getmembers

from pynject.const import PYNJECT_ATTR, PYNJECT_MODEL, PYNJECT_SINGLETON
from pynject.model import PynjectModel


def is_pynject(cls):
    return getattr(cls, PYNJECT_ATTR, False)


def is_singleton(cls):
    return getattr(cls, PYNJECT_SINGLETON, False)


def get_constructor(cls):
    for member in getmembers(cls):
        if member[0] == '__init__':
            return member[1]
    raise TypeError('class {} has no __init__ method'.format(cls))


def has_empty_construtor(cls):
    try:
        contructor = get_constructor(cls)
        if contructor == object.__init__:
            return True
        params = signature(get_constructor(cls)).parameters
        return len(params) == 1 and 'self' in params
    except TypeError:
        return True


def get_model(cls) -> PynjectModel:
    return getattr(cls, PYNJECT_MODEL)
