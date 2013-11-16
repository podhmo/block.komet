# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IViewClassifier
from pyramid.interfaces import IView
from zope.interface import Interface

def proutes(config, use_fn=logger.info):
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

