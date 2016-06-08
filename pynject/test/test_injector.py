from unittest.case import TestCase

from pynject.decorators import pynject, singleton
from pynject.injector import Injector
from pynject.module import Module


class InjectorTest(TestCase):
    def test_empty_constructor(self):
        class Foo:
            def __init__(self):
                pass

            def get_x(self):
                return 42

        injector = Injector(Module())
        foo = injector.get_instance(Foo)
        self.assertTrue(isinstance(foo, Foo))
        self.assertEqual(foo.get_x(), 42)

    def test_inject_dependencies(self):
        class Foo:
            def __init__(self):
                pass

            def get_x(self):
                return 42

        @pynject
        class Bar:
            def __init__(self, foo: Foo):
                self.foo = foo

            def get_x(self):
                return self.foo.get_x()

        injector = Injector(Module())
        bar = injector.get_instance(Bar)
        self.assertTrue(isinstance(bar, Bar))
        self.assertTrue(isinstance(bar.foo, Foo))
        self.assertEqual(bar.get_x(), 42)

    def test_inject_singleton(self):
        @singleton
        class Foo:
            def __init__(self):
                self.x = 42

        injector = Injector(Module())
        foo1 = injector.get_instance(Foo)
        foo2 = injector.get_instance(Foo)

        self.assertEqual(foo1.x, 42)

        foo2.x = 43

        self.assertEqual(foo1.x, 43)

    def test_configure_module(self):
        class Foo:
            def __init__(self):
                pass

            def get_x(self):
                pass

        class Bar(Foo):
            def __init__(self):
                super().__init__()
                pass

            def get_x(self):
                return 42

        class MyModule(Module):
            def configure(self):
                self.bind(Foo).to(Bar)

        injector = Injector(MyModule())
        foo = injector.get_instance(Foo)
        self.assertTrue(isinstance(foo, Bar))
        self.assertEqual(foo.get_x(), 42)

    def test_no_constructor(self):
        class Foo:
            def get_x(self):
                return 42

        injector = Injector(Module())
        foo = injector.get_instance(Foo)
        self.assertTrue(isinstance(foo, Foo))
        self.assertEqual(foo.get_x(), 42)
