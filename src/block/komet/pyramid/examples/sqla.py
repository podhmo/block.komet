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
    resource_factory = KometResourceFactory(ModelProducing, walking, session_factory)
    config.register_resource_factory(resource_factory, name=name)
    return resource_factory

## view category

from ..views import (
    OneModelViewFactory,
    OneModelCreationViewFactory,
    OneModelUpdatingViewFactory,
    OneModelDeletingViewFactory,
    OneModelListingViewFactory
)

def list_view_category(vcs):
    def pattern_fn(Model):
        return "/api/{}s".format(Model.__name__.lower())

    def route_name_fn(Model):
        return "{}.index".format(Model.__name__.lower())

    with vcs.define_view_category(pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.GET
        vc.define_view(OneModelListingViewFactory(parsing), renderer="json")

        def parsing(request):
            return request.POST #todo: validation
        vc.define_view(OneModelCreationViewFactory(parsing), request_method="POST", renderer="json")

def detail_view_category(vcs):
    def pattern_fn(Model):
        return "/api/{}s/{{id}}".format(Model.__name__.lower())

    def route_name_fn(Model):
        return "{}.detail".format(Model.__name__.lower())

    with vcs.define_view_category(pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.matchdict["id"]
        vc.define_view(OneModelViewFactory(parsing), request_method="GET", renderer="json")

        def parsing(request):
            return request.matchdict["id"], request.POST
        vc.define_view(OneModelUpdatingViewFactory(parsing), request_method="POST", renderer="json")

        def parsing(request):
            return request.matchdict["id"]
        vc.define_view(OneModelDeletingViewFactory(parsing), request_method="DELETE", renderer="json")
