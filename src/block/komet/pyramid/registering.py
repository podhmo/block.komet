# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
import contextlib
from .interfaces import (
    IViewCategorySetRegister,
    IViewCategoryRegister,
    IViewRegister
)

@implementer(IViewCategorySetRegister)
class ViewCategorySetRegister(object):
    def __init__(self, resource_factory):
        self.resource_factory = resource_factory
        self.registers = []

    def register(self, name, register): #todo:options?
        self.registers.append((name, register))
    __setitem__ = register

    def __call__(self, config, Model):
        resource = self.resource_factory(Model)
        for name, register in self.registers:
            register(config, Model, resource)

@implementer(IViewCategoryRegister)
class ViewCategoryRegister(object):
    def __init__(self, pattern_create, route_name_create):
        self.pattern_create = pattern_create
        self.route_name_create = route_name_create
        self.registers = []

    def register(self, name, register): #todo:options?
        self.registers.append((name, register))
    __setitem__ = register

    def __call__(self, config, Model, resource):
        route_name = self.route_name_create(Model)
        pattern = self.pattern_create(Model)
        config.add_route(route_name, pattern=pattern, factory=resource)
        logger.debug("registering.. route=%s, pattern=%s", route_name, pattern)
        for name, register in self.registers:
            register(config, Model, route_name)

@implementer(IViewRegister)
class ViewRegister(object):
    def __init__(self, view, **kwargs):
        self.view = view
        self.kwargs = kwargs

    def __call__(self, config, Model, route_name):
        config.add_view(self.view, route_name=route_name, **self.kwargs)
        logger.debug("registering.. view=%s, route=%s", self.view, route_name)
