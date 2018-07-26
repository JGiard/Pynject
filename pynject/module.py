from typing import Callable, Type, Any, Optional

from pynject.const import PYNJECT_SINGLETON
from pynject.model import PynjectAttribute


class BoundClass:
    def __init__(self, cls, target):
        self.cls = cls
        self.target = target


class ModuleStorage:
    def __init__(self):
        self.bound_cls = {}
        self.provided_cls = {}
        self.instance_cls = {}
        self.hooks = []

    def is_bound(self, cls):
        return cls in self.bound_cls

    def is_provided(self, cls):
        return cls in self.provided_cls

    def is_instancied(self, cls):
        return cls in self.instance_cls

    def get_target(self, cls):
        return self.bound_cls[cls]

    def get_provider(self, cls):
        return self.provided_cls[cls]

    def get_instance(self, cls):
        return self.instance_cls[cls]

    def add_bound_class(self, cls, target):
        self.bound_cls[cls] = target

    def add_provided_class(self, cls, target):
        self.provided_cls[cls] = target

    def add_instancied_class(self, cls, target):
        self.instance_cls[cls] = target

    def add_hook(self, hook):
        self.hooks.append(hook)


class Module:
    def __init__(self):
        self.storage = ModuleStorage()

    def configure(self):
        pass

    def configure_to(self, storage: ModuleStorage):
        self.storage = storage
        self.configure()

    def install(self, module):
        module.configure_to(self.storage)

    def bind(self, cls):
        return Binder(cls, self.storage)

    def add_hook(self, hook: Callable[[Type, PynjectAttribute], Optional[Any]]):
        self.storage.add_hook(hook)


class Binder:
    def __init__(self, cls, storage: ModuleStorage):
        self.cls = cls
        self.storage = storage

    def to(self, target):
        self.storage.add_bound_class(self.cls, target)

    def as_singleton(self):
        setattr(self.cls, PYNJECT_SINGLETON, True)

    def to_provider(self, provider):
        Binder(provider, self.storage).as_singleton()
        self.storage.add_provided_class(self.cls, provider)

    def to_instance(self, instance):
        self.storage.add_instancied_class(self.cls, instance)
