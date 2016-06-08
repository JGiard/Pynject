from unittest.case import TestCase

from pynject.decorators import pynject
from pynject.injector import Injector
from pynject.module import Module


class Toto:
    def __init__(self):
        pass

    def get_toto(self):
        return 'toto'


class Toto2(Toto):
    def get_toto(self):
        return 'toto2'


@pynject
class Titi:
    def __init__(self, toto: Toto):
        self.toto = toto

    def get_titi(self):
        return 'titi' + self.toto.get_toto()


class MyModule(Module):
    def configure(self):
        self.bind(Toto).to(Toto2)


class TitiTest(TestCase):
    def test(self):
        injector = Injector(MyModule())
        titi = injector.get_instance(Titi)
        self.assertEquals(titi.get_titi(), 'tititoto2')
