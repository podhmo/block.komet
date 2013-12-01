# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import venusian
from zope.interface import (
    implementer,
    provider
)
from ..interfaces import (
    IDisplayMessage,
    IFailure,
)

from ..utils import nameof

from .interfaces import (
    IValidationGenerator,
)

@provider(IValidationGenerator)
def _sample_validation_generator(request, kwargs):
    """ sample function"""
    unique_name = lambda data, id=None: True #dummy
    if "id" in kwargs:
        yield "name", lambda data: unique_name(data, id=kwargs["id"])
    else:
        yield "name", unique_name

def message_from_errors(errors):
    r = []
    for k, vs in errors.items():
        sr = "\t".join(vs)
        if sr:
            r.append(k)
            r.append("\t"+sr)
    return "\n".join(r)


## hmmm.
def add_display_message(config, exception, message):
    implementer(IFailure)(exception) #xxx:
    def register_display_message():
        adapters = config.registry.adapters
        adapters.register([IFailure], IDisplayMessage, nameof(exception), message)

    discriminator = nameof(exception)
    desc = "human redable message for {}".format(nameof(exception))
    introspectables = [
        config.introspectable('display_messages', discriminator, desc, 'display_message')
    ]
    config.action(discriminator, register_display_message, introspectables=introspectables)

def display_message_config(exception):
    def _wrapped(message_fn):
        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_display_message(exception, message_fn)
        info = venusian.attach(message_fn, callback, category='pyramid') #xxx:
        return message_fn
    return _wrapped

def includeme(config):
    config.add_directive("add_display_message", add_display_message)

