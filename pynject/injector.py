from pynject.helpers import has_empty_construtor, is_pynject, get_model
from pynject.module import Module


class Injector:
    def __init__(self, module: Module):
        module.configure()
        self.module = module

    def get_instance(self, cls):
        if self.module.is_bound(cls):
            return self.get_instance(self.module.get_target(cls))
        if has_empty_construtor(cls):
            return cls()
        elif is_pynject(cls):
            model = get_model(cls)
            params = {}
            for attribute in model.attributes:
                params[attribute.name] = self.get_instance(attribute.attr_type)
            return cls(**params)
        else:
            raise TypeError('class {} has no pynject information'.format(cls))
