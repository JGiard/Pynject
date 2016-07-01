from unittest import TestCase

from pynject.helpers import is_singleton
from pynject.module import Module, ModuleStorage, Binder


class TestClass:
    pass


class TargetClass:
    pass


class ModuleStorageTest(TestCase):
    def setUp(self):
        self.storage = ModuleStorage()

    def test_not_bound_class(self):
        self.assertFalse(self.storage.is_bound(TestClass))
        self.assertFalse(self.storage.is_provided(TestClass))
        self.assertFalse(self.storage.is_instancied(TestClass))

    def test_bind_one_class(self):
        self.storage.add_bound_class(TestClass, TargetClass)
        self.assertTrue(self.storage.is_bound(TestClass))
        self.assertEqual(self.storage.get_target(TestClass), TargetClass)

    def test_provide_one_class(self):
        self.storage.add_provided_class(TestClass, TargetClass)
        self.assertTrue(self.storage.is_provided(TestClass))
        self.assertEqual(self.storage.get_provider(TestClass), TargetClass)

    def test_instance_one_class(self):
        foo = TestClass()
        self.storage.add_instancied_class(TestClass, foo)
        self.assertTrue(self.storage.is_instancied(TestClass))
        self.assertEqual(self.storage.get_instance(TestClass), foo)

    def test_bind_multiple_classes(self):
        class Foo:
            pass

        class Bar:
            pass

        self.storage.add_bound_class(TestClass, TargetClass)
        self.storage.add_bound_class(Foo, Bar)

        self.assertTrue(self.storage.is_bound(TestClass))
        self.assertTrue(self.storage.is_bound(Foo))

        self.assertEqual(self.storage.get_target(TestClass), TargetClass)
        self.assertEqual(self.storage.get_target(Foo), Bar)


class BinderTest(TestCase):
    def setUp(self):
        self.storage = ModuleStorage()

    def test_bind_to(self):
        Binder(TestClass, self.storage).to(TargetClass)

        self.assertTrue(self.storage.is_bound(TestClass))
        self.assertEqual(self.storage.get_target(TestClass), TargetClass)

    def test_as_singleton(self):
        class Foo:
            pass

        Binder(Foo, self.storage).as_singleton()
        self.assertTrue(is_singleton(Foo))

    def test_to_provider(self):
        class Foo:
            pass

        class FooProvider:
            pass

        Binder(Foo, self.storage).to_provider(FooProvider)
        self.assertTrue(self.storage.is_provided(Foo))
        self.assertTrue(is_singleton(FooProvider))
        self.assertEqual(self.storage.get_provider(Foo), FooProvider)

    def test_to_instance(self):
        foo = TestClass()
        Binder(TestClass, self.storage).to_instance(foo)

        self.assertTrue(self.storage.is_instancied(TestClass))
        self.assertEqual(self.storage.get_instance(TestClass), foo)


class ModuleTest(TestCase):
    def test_delegate_install(self):
        class ModuleB(Module):
            def configure(self):
                self.bind(TestClass).to(TargetClass)

        class ModuleA(Module):
            def configure(self):
                self.install(ModuleB())

        moduleA = ModuleA()
        moduleA.configure()

        self.assertTrue(moduleA.storage.is_bound(TestClass))
        self.assertEqual(moduleA.storage.get_target(TestClass), TargetClass)
