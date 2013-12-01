# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from pyramid.decorator import reify
from functools import partial
import contextlib
from zope.interface import (
    implementer,
)
from .interfaces import IResourceFactory

from block.komet.exceptions import NotFoundFailure
from ..utils import nameof
from ..utils import provided_chain
from ..utils import get_support_options
from block.form.validation import get_validation

@implementer(IResourceFactory)
class KometResourceFactory(object):
    def __init__(self, producing, walking, session_factory):
        self.producing = producing
        self.walking = walking
        self.session_factory = session_factory

    @reify
    def available_options(self):
        return {k: get_support_options(getattr(self, k)) for k in ["producing", "walking"]}

    def __call__(self, Model):
        logger.info("available.. {}".format(self.available_options))
        return partial(KommetResource, self, Model)

class KommetResource(object):
    def __init__(self, env, Model, request):
        self.env = env
        self.Model = Model
        self.request = request

    @reify
    def session(self):
        return self.env.session_factory(self.request)

    @reify
    def producing(self):
        return self.env.producing(self.session, self.Model)

    @reify
    def walking(self):
        return self.env.walking

    def raise_exception(self, exc):
        raise exc

    @contextlib.contextmanager
    def try_maybe_notfound(self, exception, fallback=raise_exception):
        try:
            yield
        except NotFoundFailure:
            return fallback(self, exception("not found. {}".format(nameof(self.Model))))

    def try_commit(self, parsing, params, commit, **extra):
        required = (next(provided_chain(parsing, self.request)), )
        validation = get_validation(self.request, required, name=nameof(self.Model))
        validation.extra["session"] = self.session
        if validation:
            params = validation.validate(params, **extra)
        return commit(params)

def register_resource_factory(config, resource_factory, name=""):
    config.registry.registerUtility(resource_factory, IResourceFactory, name=name)

def get_resource_factory(config, name=""):
    return config.registry.getUtility(IResourceFactory, name=name)

def includeme(config):
    config.add_directive("register_resource_factory", register_resource_factory)
    config.add_directive("get_resource_factory", get_resource_factory)
