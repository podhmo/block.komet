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

def list_view_category(vcs, name):
    def pattern_fn(Model):
        return "/api/{}s".format(nameof(Model).lower())

    def route_name_fn(Model):
        return "{}.index".format(nameof(Model).lower())

    with vcs.define_view_category(name, pattern_fn, route_name_fn) as vc:
        def parsing_get(request):
            return request.GET
        with vc.define_view("list", OneModelListingViewFactory, renderer="json") as v:
            @v.register
            def callback(view_factory, Model, options):
                query_options = vcs.get_supported_options(options, "producing")
                return view_factory(parsing_get, query_options)

        def parsing_post(request):
            return request.POST #todo: validation
        with vc.define_view("create", OneModelCreationViewFactory, request_method="POST", renderer="json") as v:
            @v.register
            def callback(view_factory, Model, options):
                return view_factory(parsing_post)

def detail_view_category(vcs, name):
    def pattern_fn(Model):
        return "/api/{}s/{{id}}".format(nameof(Model).lower())

    def route_name_fn(Model):
        return "{}.detail".format(nameof(Model).lower())

    with vcs.define_view_category(name, pattern_fn, route_name_fn) as vc:
        def parsing_matchdict(request):
            return request.matchdict["id"]
        with vc.define_view("info", OneModelViewFactory, request_method="GET", renderer="json") as v:
            @v.register
            def callback(view_factory, Model, options):
                return view_factory(parsing_matchdict)
        def parsing(request):
            return request.matchdict["id"], request.POST
        with vc.define_view("update", OneModelUpdatingViewFactory, request_method="POST", renderer="json") as v:
            @v.register
            def callback(view_factory, Model, options):
                return view_factory(parsing)
        with vc.define_view("delete", OneModelDeletingViewFactory, request_method="DELETE", renderer="json") as v:
            @v.register
            def callback(view_factory, Model, options):
                return view_factory(parsing_matchdict)
