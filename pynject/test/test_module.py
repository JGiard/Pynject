from unittest import TestCase

from helpers import is_singleton
from pynject.module import Module


class ModuleTest(TestCase):
    def test_bind_to(self):
        class TestClass:
            pass

        module = Module()
        module.bind(TestClass).to(42)

        self.assertTrue(module.is_bound(TestClass))
        self.assertEqual(module.get_target(TestClass), 42)

    def test_bind_singleton(self):
        class TestClass:
            pass

        module = Module()
        module.bind(TestClass).as_singleton()

        self.assertTrue(is_singleton(TestClass))
