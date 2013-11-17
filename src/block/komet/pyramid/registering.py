# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from .interfaces import (
    IViewCategorySetRegister,
    IViewCategoryRegister,
    IViewRegister,
    IRegisterRepository
)
from collections import namedtuple
import contextlib
from pyramid.decorator import reify
from ..utils import nameof

@implementer(IViewCategorySetRegister)
class ViewCategorySetRegister(object):
    def __init__(self, name, resource_factory):
        self.resource_factory = resource_factory
        self.registers = []
        self.name = name

    def register(self, register): #todo:options?
        self.registers.append(register)

    def __call__(self, config, Model, options):
        resource = self.resource_factory(Model)
        for register in self.registers:
            sub_options = options.get(register.name, {})
            register(config, Model, resource, options=sub_options)

@implementer(IViewCategoryRegister)
class ViewCategoryRegister(object):
    def __init__(self, name, pattern_create, route_name_create):
        self.pattern_create = pattern_create
        self.route_name_create = route_name_create
        self.registers = []
        self.name = name

    def register(self, register): #todo:options?
        self.registers.append(register)


    def __call__(self, config, Model, resource, options):
        route_name = self.route_name_create(Model)
        pattern = self.pattern_create(Model)
        config.add_route(route_name, pattern=pattern, factory=resource)
        logger.debug("registering.. route=%s, pattern=%s", route_name, pattern)
        for register in self.registers:
            sub_options = options.get(register.name, {})
            register(config, Model, route_name, options=sub_options)

@implementer(IViewRegister)
class ViewRegister(object):
    def __init__(self, name, view, **kwargs):
        self.name = name
        self.view = view
        self.kwargs = kwargs
        self.name = "{}ViewRegister".format(nameof(view))

    def __call__(self, config, Model, route_name, options):
        logger.info(".. options %s", options)
        config.add_view(self.view, route_name=route_name, **self.kwargs)
        logger.debug("registering.. view=%s, route=%s", self.view, route_name)

_RegisterRepository = namedtuple("RegisterRepository", "view_category_set, view_category, view")
RegisterRepository = implementer(IRegisterRepository)(_RegisterRepository)

class _RegisterProxy(object):
    def __init__(self, core, repository):
        self.core = core
        self.repository = repository

    def __getattr__(self, k):
        return getattr(self.core, k)

    def __call__(self, *args, **kwargs):
        return self.core(*args, **kwargs)

class ViewCategorySetRegisterProxy(_RegisterProxy):
    @contextlib.contextmanager
    def define_view_category(self, name, patten_create, route_name_create, **kwargs):
        parent = self.core
        factory = self.repository.view_category
        child = factory(name, patten_create, route_name_create, **kwargs)
        parent.register(child)
        yield ViewCategoryRegisterProxy(child, self.repository)

class ViewCategoryRegisterProxy(_RegisterProxy):
    def define_view(self, *args, **kwargs):
        parent = self.core
        factory = self.repository.view
        child = factory(*args, **kwargs)
        parent.register(child)
        return child

class ViewRegisteringBuilder(object):
    RegisterProxy = ViewCategorySetRegisterProxy
    def __init__(self, config, name, resource_factory):
        self.config = config
        self.resource_factory = resource_factory
        self.name = name

    @reify
    def repository(self):
        return self.config.registry.getUtility(IRegisterRepository)

    @reify
    def view_category_set(self):
        factory = self.repository.view_category_set
        return self.RegisterProxy(factory(self.name, self.resource_factory), self.repository)

    def build(self, config, Model, options=None):
        options = options or {}
        self.view_category_set(config, Model, options=options)


def includeme(config, name=""):
    repo = RegisterRepository(
        view_category_set=ViewCategorySetRegister,
        view_category=ViewCategoryRegister,
        view=ViewRegister
    )
    config.registry.registerUtility(repo, IRegisterRepository, name=name)

    ## install view registering builder
    config.add_directive("view_registering_builder", ViewRegisteringBuilder)
