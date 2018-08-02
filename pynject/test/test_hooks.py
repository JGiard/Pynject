from unittest.case import TestCase

from pynject import Module, Injector, pynject
from pynject.model import PynjectAttribute


class HookTest(TestCase):
    def test_simple_hook(self):
        @pynject
        class Toto:
            def __init__(self, foo: 'bar'):
                self.foo = foo

        def my_hook(cls, attr: PynjectAttribute):
            if issubclass(cls, Toto) and attr.name == 'foo':
                return 5

        class MyModule(Module):
            def configure(self):
                self.add_hook(my_hook)

        toto = Injector(MyModule()).get_instance(Toto)

        assert toto.foo == 5

    def test_simple_hook_with_no_type(self):
        @pynject
        class Toto:
            def __init__(self, foo):
                self.foo = foo

        def my_hook(cls, attr: PynjectAttribute):
            if issubclass(cls, Toto) and attr.name == 'foo':
                return 5

        class MyModule(Module):
            def configure(self):
                self.add_hook(my_hook)

        toto = Injector(MyModule()).get_instance(Toto)

        assert toto.foo == 5
