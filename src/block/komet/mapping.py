# -*- coding:utf-8 -*-
from functools import wraps, partial
from . import interfaces as i
from .utils import normalize_registry, normalize_provided

def includeme(config):
    config.include(install_json_mapping)

#util

def get_mapping_function_factory(request_or_registry, name=""):
    registry = normalize_registry(request_or_registry)
    def mapping(provided):
        provided = normalize_provided(provided)
        return registry.adapters.lookup(provided, i.IMapping, name=name)
    return mapping


def maybe_None(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except TypeError:
            if args[0] is None:
                return "null"
            raise
    return wrapper

@maybe_None
def isoformat(d):
    return d.isoformat()

def json_null(x):
    return "null"
@maybe_None
def json_boolean(x):
    return "true" if bool(x) else "false"
@maybe_None
def json_int(x):
    return str(int(x))
@maybe_None
def json_list(xs, convert):
    return str(list(convert(x) for x in xs))
@maybe_None
def json_float(x):
    return str(float(x))
@maybe_None
def json_string(x):
    return '"{}"'.format(x)

def install_json_mapping(config):
    adapters = config.registry.adapters
    name = "json"
    adapters.register([i.IUnknown], i.IMapping, name, lambda x: "???")
    adapters.register([i.IBytes], i.IMapping, name, bytes) #xxx:
    adapters.register([i.IString], i.IMapping, name, json_string)
    adapters.register([i.IBoolean], i.IMapping, name, json_boolean)
    adapters.register([i.INothing], i.IMapping, name, json_null)
    adapters.register([i.IInteger], i.IMapping, name, json_int)
    adapters.register([i.IFloat], i.IMapping, name, json_float)
    adapters.register([i.IDateTime], i.IMapping, name, isoformat)
    adapters.register([i.IDate], i.IMapping, name, isoformat)
    adapters.register([i.ITime], i.IMapping, name, isoformat)

    adapters.register([i.IInteger, i.IInteger], i.IMapping, name, partial(json_list, convert=json_int))
    adapters.register([i.IString, i.IString], i.IMapping, name, partial(json_list, convert=json_string))
