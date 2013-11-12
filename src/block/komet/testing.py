# -*- coding:utf-8 -*-
from zope.interface.registry import Components
import contextlib 

class DummyConfig(object):
    def __init__(self, registry):
        self.registry = registry

    def include(self, target):
        if callable(target):
            return target(self)
        raise NotImplementedError("sorry. %s", target)

def setUp(registry=None, settings=None):
    registry = registry or Components()
    registry.settings = settings or {}
    return DummyConfig(registry)

def tearDown():
    pass

@contextlib.contextmanager
def test_config(*args, **kwargs):
    config = setUp(*args, **kwargs)
    yield config
    tearDown()
