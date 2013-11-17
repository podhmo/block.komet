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
from block.komet.utils import nameof

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
        return "/api/{}s".format(nameof(Model).lower())

    def route_name_fn(Model):
        return "{}.index".format(nameof(Model).lower())

    with vcs.define_view_category("index", pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.GET
        vc.define_view("list", OneModelListingViewFactory(parsing), renderer="json")

        def parsing(request):
            return request.POST #todo: validation
        vc.define_view("create", OneModelCreationViewFactory(parsing), request_method="POST", renderer="json")

def detail_view_category(vcs):
    def pattern_fn(Model):
        return "/api/{}s/{{id}}".format(nameof(Model).lower())

    def route_name_fn(Model):
        return "{}.detail".format(nameof(Model).lower())

    with vcs.define_view_category("detail", pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.matchdict["id"]
        vc.define_view("info", OneModelViewFactory(parsing), request_method="GET", renderer="json")

        def parsing(request):
            return request.matchdict["id"], request.POST
        vc.define_view("update", OneModelUpdatingViewFactory(parsing), request_method="POST", renderer="json")

        def parsing(request):
            return request.matchdict["id"]
        vc.define_view("delete", OneModelDeletingViewFactory(parsing), request_method="DELETE", renderer="json")
