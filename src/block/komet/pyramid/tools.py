# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IViewClassifier
from pyramid.interfaces import IView
from zope.interface import Interface
from ..utils import nameof
import sys

def perror(*args):
    for e in args:
        sys.stderr.write(e)
    sys.stderr.write("\n")

def proutes(config, use_fn=perror):
    mapper = config.get_routes_mapper()
    registry = config.registry
    if mapper is not None:
        routes = mapper.get_routes()
        assert routes
        fmt = '%-15s %-30s %-25s'
        if not routes:
            return 0
        use_fn(fmt % ('Name', 'Pattern', 'View'))
        use_fn(
            fmt % ('-'*len('Name'), '-'*len('Pattern'), '-'*len('View')))
        for route in routes:
            pattern = route.pattern
            if not pattern.startswith('/'):
                pattern = '/' + pattern
            request_iface = registry.queryUtility(IRouteRequest,
                                                  name=route.name)
            view_callable = None
            if (request_iface is None) or (route.factory is not None):
                use_fn(fmt % (route.name, pattern, '<unknown>'))
            else:
                view_callable = registry.adapters.lookup(
                    (IViewClassifier, request_iface, Interface),
                    IView, name='', default=None)
                use_fn(fmt % (route.name, pattern, view_callable))

def pkomets(config, use_fn=perror): #todo.rename
    fmt = '%-20s %-45s'
    komets = config.registry.introspector.get_category("komets", sort_key=lambda x: x["Target"].__name__)
    if not komets:
        return 0

    intrs = (k["introspectable"] for k in komets)
    import itertools
    for (g, vs) in itertools.groupby(intrs, lambda x: x["Target"]):
        use_fn("------------------------------------------------------------")
        use_fn("%s::" % nameof(g))
        use_fn(fmt % ('Name', 'Options'))
        use_fn(fmt % ('-'*len('Name'), '-'*len('Options')))
        for intr in vs:
            use_fn(fmt % (intr.discriminator, intr["options"]))
