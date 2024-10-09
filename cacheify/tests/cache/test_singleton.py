import pytest
from cacheify.cache.singleton import Singleton

class ExampleClass(metaclass=Singleton):
    def __init__(self, value):
        self.value = value

def test_singleton_same_instance():
    instance1 = ExampleClass(1)
    instance2 = ExampleClass(1)
    assert instance1 is instance2
    assert instance1.value == instance2.value

def test_singleton_different_instances():
    instance1 = ExampleClass(1)
    instance2 = ExampleClass(2)
    assert instance1 is not instance2
    assert instance1.value != instance2.value

def test_singleton_with_kwargs():
    instance1 = ExampleClass(value=1)
    instance2 = ExampleClass(value=1)
    assert instance1 is instance2
    assert instance1.value == instance2.value

def test_singleton_different_kwargs():
    instance1 = ExampleClass(value=1)
    instance2 = ExampleClass(value=2)
    assert instance1 is not instance2
    assert instance1.value != instance2.value