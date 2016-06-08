import re
from inspect import signature, getmembers

from pynject.const import PYNJECT_ATTR, PYNJECT_MODEL
from pynject.model import PynjectModel


def is_pynject(obj_type):
    return getattr(obj_type, PYNJECT_ATTR, False)


def get_constructor(cls):
    for member in getmembers(cls):
        if member[0] == '__init__':
            return member[1]
    raise TypeError('class {} has no __init__ method'.format(cls))


def has_empty_construtor(cls):
    try:
        params = signature(get_constructor(cls)).parameters
        return len(params) == 1 and 'self' in params
    except TypeError:
        return True


def get_model(cls) -> PynjectModel:
    return getattr(cls, PYNJECT_MODEL)
