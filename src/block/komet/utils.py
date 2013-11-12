# -*- coding:utf-8 -*-
from zope.interface.interface import InterfaceClass
from zope.interface import providedBy

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
