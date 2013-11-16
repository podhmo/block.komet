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
