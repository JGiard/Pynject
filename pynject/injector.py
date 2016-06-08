from helpers import is_singleton
from pynject.helpers import has_empty_construtor, is_pynject, get_model
from pynject.module import Module


class Injector:
    def __init__(self, module: Module):
        module.configure()
        self.module = module
        self.singletons = {}

    def get_instance(self, cls):
        if self.module.is_bound(cls):
            return self.get_instance(self.module.get_target(cls))
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
                params[attribute.name] = self.get_instance(attribute.attr_type)
            obj = cls(**params)

        if is_singleton(cls):
            self.singletons[cls] = obj
        return obj
