from const import PYNJECT_SINGLETON


class BoundClass:
    def __init__(self, cls, target):
        self.cls = cls
        self.target = target


class Module:
    def __init__(self):
        self.bound_cls = {}

    def is_bound(self, cls):
        return cls in self.bound_cls

    def get_target(self, cls):
        return self.bound_cls[cls]

    def configure(self):
        pass

    def add_bound_class(self, cls, target):
        self.bound_cls[cls] = target

    def bind(self, cls):
        return Binder(cls, self)


class Binder:
    def __init__(self, cls, module: Module):
        self.cls = cls
        self.module = module

    def to(self, target):
        self.module.add_bound_class(self.cls, target)

    def as_singleton(self):
        setattr(self.cls, PYNJECT_SINGLETON, True)
