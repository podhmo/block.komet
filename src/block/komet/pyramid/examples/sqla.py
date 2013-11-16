# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from block.komet.sqla import (
    MapperWalking,
    ColumnsWalkingTemplate,
    ModelProducing
)
from block.komet.pyramid.resources import (
    KometResourceFactory
)

def install_komet_resource(config, session_factory, mapping, name=""):
    config.include("block.komet.pyramid.resources")
    walking = MapperWalking(ColumnsWalkingTemplate, mapping)
    producing = ModelProducing(session_factory)
    resource_factory = KometResourceFactory(producing, walking)
    config.register_resource_factory(resource_factory, name=name)
    return resource_factory

## view category
from ..views import OneModelViewFactory

def detail_view_category(vcs):
    def pattern_fn(Model):
        return "/{}/{{id}}".format(Model.__name__.lower())

    def route_name_fn(Model):
        return "{}.detail".format(Model.__name__.lower())

    with vcs.define_view_category(pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.matchdict["id"]
        vc.define_view(OneModelViewFactory(parsing), request_method="GET", renderer="json")
