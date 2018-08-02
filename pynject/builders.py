import sys
from inspect import Parameter, signature

from pynject.helpers import get_constructor
from pynject.model import PynjectModel, PynjectAttribute, PynjectUnresolvedAttribute


def type_provider(cls, name):
    def resolver():
        try:
            return getattr(sys.modules[cls.__module__], name)
        except AttributeError:
            raise TypeError('could not resolve string annotation {} in class {}'.format(name, cls.__name__))

    return resolver


class PynjectModelBuilder:
    def __init__(self, cls):
        self.cls = cls

    def build_model(self) -> PynjectModel:
        constructor = get_constructor(self.cls)
        attributes = []
        for name, parameter in signature(constructor).parameters.items():
            if name != 'self':
                attribute = self.build_attribute(parameter)
                attributes.append(attribute)
        return PynjectModel(attributes)

    def build_attribute(self, parameter: Parameter) -> PynjectAttribute:
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pynject only handle named parameters')
        if type(parameter.annotation) is str:
            return PynjectUnresolvedAttribute(parameter.name, type_provider(self.cls, parameter.annotation))
        return PynjectAttribute(parameter.name, parameter.annotation)
