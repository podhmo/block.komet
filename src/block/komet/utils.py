# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface.interface import InterfaceClass
from zope.interface import providedBy


def nameof(o):
    try:
        return o.__name__
    except AttributeError as e:
        logger.debug(repr(e))
        return o.__class__.__name__

import itertools
def provided_chain(*xs):
    return itertools.chain.from_iterable((normalize_provided1(x) for x in xs))

def define_support_options(**kwargs):
    def _wrapped(cls):
        if not hasattr(cls, "_support_options"):
            cls._support_options = {}
        cls._support_options.update(kwargs)
        return cls
    return _wrapped

def get_support_options(cls):
    if not hasattr(cls, "_support_options"):
        return {}
    return cls._support_options

def checked_suported_options(options, supported_options, category, Error=Exception):
    try:
        available_options = supported_options[category]
    except KeyError:
        fmt = "category '{}' is not supported. (available categories = {})"
        raise Error(fmt.format(category, tuple(supported_options.keys())))

    enable_options = {}
    for k, v in options.get(category, {}).items():
        if not k in available_options:
            fmt = "option '{}' is not supported, in category={}. (available options = {})"
            raise Error(fmt.format(k, category, available_options))
        enable_options[k] = v
    return enable_options


def normalize_registry(request_or_registry):
    if hasattr(request_or_registry, "registry"):
        return request_or_registry.registry
    else:
        return request_or_registry

def normalize_provided1(provided):
    if isinstance(provided, InterfaceClass):
        return provided
    else:
        return providedBy(provided)

def normalize_provided(provided):
    if hasattr(provided, "__len__"):
        return [normalize_provided1(p) for p in provided]
    else:
        return [normalize_provided1(provided)]
