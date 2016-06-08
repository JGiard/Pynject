import sys
from inspect import Parameter, getmembers, signature

from pynject.const import PYNJECT_TYPEINFO
from pynject.helpers import get_constructor
from pynject.model import PynjectModel, PynjectAttribute, ListType, UnresolvedListType, PynjectUnresolvedAttribute


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
        self.type_info = getattr(cls, PYNJECT_TYPEINFO, dict())

    def build_model(self) -> PynjectModel:
        constructor = get_constructor(self.cls)
        attributes = []
        for name, parameter in signature(constructor).parameters.items():
            if name != 'self':
                attribute = self.build_attribute(parameter)
                attributes.append(attribute)
        return PynjectModel(attributes)

    def build_attribute(self, parameter: Parameter) -> PynjectAttribute:
        if parameter.annotation is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(parameter.name, self.cls.__name__))
        if parameter.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError('pynject only handle named parameters')
        if parameter.annotation is list:
            if parameter.name in self.type_info:
                sub_type = self.type_info[parameter.name]
                attr_type = ListType(sub_type)
                if type(sub_type) is str:
                    attr_type = UnresolvedListType(type_provider(self.cls, sub_type))
                return PynjectAttribute(parameter.name, attr_type)
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(parameter.name,
                                                                                      self.cls.__name__))
        if type(parameter.annotation) is str:
            return PynjectUnresolvedAttribute(parameter.name, type_provider(self.cls, parameter.annotation))
        return PynjectAttribute(parameter.name, parameter.annotation)
