# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
import venusian
from zope.interface import (
    implementedBy,
    providedBy,
    implementer,
    provider
)
from ..interfaces import (
    IValidating,
    IDisplayMessage,
    IFailure,
    IHasMessage
)

from ..utils import nameof
from ..exceptions import ValidationFailure
from ..exceptions import BadData

from .interfaces import IValidationGenerator

@provider(IValidationGenerator)
def _sample_validation_generator(request, kwargs):
    """ sample function"""
    unique_name = lambda data, id=None: True #dummy
    if "id" in kwargs:
        yield "name", lambda data: unique_name(data, id=kwargs["id"])
    else:
        yield "name", unique_name

@implementer(IValidationGenerator)
class ValidationQueue(object):
    def __init__(self):
        self.q = []

    def add(self, name, validation, pick=None):
        validation_factory = self.normalize(validation, pick)
        validation_factory.__name__ =  "V_{}".format(validation.__name__)
        self.q.append((name, validation_factory))
        return self

    def normalize(self, validation, pick):
        if pick:
            def validation_with_extra(request, kwargs):
                def _wrapped(data):
                    extra = pick(request, data, kwargs)
                    return validation(data, **extra)
                return _wrapped
            return validation_with_extra
        else:
            def validation_simple(request, kwargs):
                return lambda data : validation(data)
            return validation_simple

    def __call__(self, request, kwargs):
        for name, v_fn in self.q:
            yield name, v_fn(request, kwargs)

def append_error_handler(request, errors, name, e):
    message = get_display_message(request, e) #todo error handling
    if name in errors:
        errors[name].append(message)
    else:
        errors[name] = [message]

def message_from_errors(errors):
    r = []
    for k, vs in errors.items():
        sr = "\t".join(vs)
        if sr:
            r.append(k)
            r.append("\t"+sr)
    return "\n".join(r)

def handle_result_default(status, data, errors, first_error):
    if status:
        return data
    else:
        message = message_from_errors(errors)
        raise ValidationFailure(message, first_error)

@implementer(IValidating)
class ValidationExecuter(object):
    def __init__(self,
                 validation_generator,
                 handle_result=handle_result_default,
                 error_handler=append_error_handler,
                 Error=BadData):
        self.validation_generator = validation_generator
        self.handle_result = handle_result
        self.error_handler = error_handler
        self.Error = Error

    def __call__(self, request, data, errors, **kwargs):
        status = True
        first_error = None
        for name, v in self.validation_generator(request, kwargs):
            try:
                v(data)
            except self.Error as e:
                status = False
                first_error = e
                self.error_handler(request, errors, name, e)
        return self.handle_result(status, data, errors, first_error)


def get_display_message(request, exception):
    adapters = request.registry.adapters
    fn = adapters.lookup1(providedBy(exception), IDisplayMessage, name=nameof(exception.__class__))
    fn = fn or adapters.lookup1(providedBy(exception), IDisplayMessage, name="")
    return fn(exception)

def default_message(exception):
    ## display stack trace?
    return repr(exception)

def message(message):
    return message.message

def add_display_message(config, exception, message):
    implementer(IFailure)(exception) #xxx:
    def register_display_message():
        adapters = config.registry.adapters
        adapters.register([IFailure], IDisplayMessage, nameof(exception), message)

    discriminator = exception
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
    config.registry.adapters.register([IFailure], IDisplayMessage, "", default_message)
    config.registry.adapters.register([IHasMessage], IDisplayMessage, "", message)
