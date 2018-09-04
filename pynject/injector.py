from inspect import Parameter

from pynject.decorators import pynject, singleton
from pynject.helpers import has_empty_construtor, is_pynject, get_model, is_singleton
from pynject.model import PynjectAttribute
from pynject.module import Module


@pynject
@singleton
class Injector:
    def __init__(self, module: Module):
        module.configure()
        self.module = module
        self.singletons = {self.__class__: self}

    def get_instance(self, cls):
        if self.module.storage.is_bound(cls):
            return self.get_instance(self.module.storage.get_target(cls))
        if self.module.storage.is_provided(cls):
            provider = self.get_instance(self.module.storage.get_provider(cls))
            return provider.get()
        if self.module.storage.is_instancied(cls):
            return self.module.storage.get_instance(cls)
        if has_empty_construtor(cls) or is_pynject(cls):
            return self.__create_class(cls)
        else:
            raise TypeError('class {} has no pynject information'.format(cls))

    def __create_class(self, cls):
        if is_singleton(cls) and cls in self.singletons:
            return self.singletons[cls]
        if has_empty_construtor(cls):
            obj = cls()
        else:
            model = get_model(cls)
            params = {}
            for attribute in model.attributes:
                params[attribute.name] = self.__fill_parameter(cls, attribute)
            obj = cls(**params)

        if is_singleton(cls):
            self.singletons[cls] = obj
        return obj

    def __fill_parameter(self, cls, attribute: PynjectAttribute):
        for hook in self.module.storage.hooks:
            instance = hook(cls, attribute)
            if instance is not None:
                return instance

        if attribute.attr_type is Parameter.empty:
            raise TypeError('parameter {} in class {} has no type'.format(attribute.name, cls.__name__))
        return self.get_instance(attribute.attr_type)
