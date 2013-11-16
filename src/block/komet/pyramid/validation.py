# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from zope.interfaces import (
    implementer,
    provider
)
from .interfaces import IValidationGenerator
from ..interfaces import IValidating
from ..exceptions import ValidationFailure

def append_error_handler(request, errors, name, e):
    if name in errors:
        errors[name].append(repr(e)) #todo error handling
    else:
        errors[name] = [repr(e)]

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

    def normalize(self, validation, pick):
        if pick:
            def validation_with_extra(request, kwargs):
                def _wrapped(data):
                    extra = pick(request, data, kwargs)
                    return validation(data, extra)
                return _wrapped
            return validation_with_extra
        else:
            def validation_simple(request, kwargs):
                return lambda data : validation(data)
            return validation_simple

    def __call__(self, request, kwargs):
        for name, v_fn in self.q:
            yield name, v_fn(request, kwargs)

@implementer(IValidating)
class ValidationExecuter(object):
    def __init__(self, 
                 validation_generator,
                 error_handler=append_error_handler,
                 Error=ValidationFailure):
        self.validation_generator = validation_generator
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
        if status:
            return data
        else:
            raise ValidationFailure(errors, first_error)
