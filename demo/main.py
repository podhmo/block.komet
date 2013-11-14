# -*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

Session = orm.sessionmaker()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    name = sa.Column(sa.String(255), unique=True, nullable=False)


from pyramid.config import Configurator

def setup_database(config):
    engine = sa.create_engine('sqlite://', echo=True)
    Session.configure(bind=engine, autoflush=False)
    Base.metadata.bind = engine
    Base.metadata.create_all()


    session = Session()
    session.add(User(name="foo"))
    session.add(User(name="boo"))
    session.add(User(name="bar"))
    session.commit()

def session_factory():
    return Session()

def setup_views(config):
    from block.komet.sqla import (
        MapperWalking, 
        ColumnsWalkingTemplate, 
        ModelProducing
    )
    from block.komet.mapping import (
        get_mapping_function_factory
    )
    from block.komet.pyramid.registering import (
        ViewCategorySetRegister, 
        ViewCategoryRegister, 
        ViewRegister
    )
    from block.komet.pyramid.resources import (
        KometResourceFactory
    )
    from block.komet.pyramid.views import (
        OneModelViewFactory
    )

    json_mapping = get_mapping_function_factory(config, name="json")

    walking = MapperWalking(ColumnsWalkingTemplate, json_mapping)
    producing = ModelProducing(session_factory)
    resource_factory = KometResourceFactory(producing, walking)

    ## todo suppress import.
    def parsing(request):
        return request.matchdict["id"]

    vcs = ViewCategorySetRegister(resource_factory)
    def pattern_fn(Model):
        return "/{}/{{id}}".format(Model.__name__.lower())

    def route_name_fn(Model):
        return "{}.detail".format(Model.__name__.lower())
    vc = ViewCategoryRegister(pattern_fn, route_name_fn)
    vcs["detail"] = vc

    v = ViewRegister(OneModelViewFactory(parsing), renderer="json")
    vc["get"] = v


    ## register
    vcs(config, User)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    from block.komet.mapping import install_json_mapping
    config.include(install_json_mapping)
    config.include(setup_database)
    config.include(setup_views)
    config.commit()

    from pyramid.interfaces import IRouteRequest
    from pyramid.interfaces import IViewClassifier
    from pyramid.interfaces import IView
    from zope.interface import Interface

    mapper = config.get_routes_mapper()
    registry = config.registry
    if mapper is not None:
        routes = mapper.get_routes()
        assert routes
        fmt = '%-15s %-30s %-25s'
        if not routes:
            return 0
        logger.info(fmt % ('Name', 'Pattern', 'View'))
        logger.info(
            fmt % ('-'*len('Name'), '-'*len('Pattern'), '-'*len('View')))
        for route in routes:
            pattern = route.pattern
            if not pattern.startswith('/'):
                pattern = '/' + pattern
            request_iface = registry.queryUtility(IRouteRequest,
                                                  name=route.name)
            view_callable = None
            if (request_iface is None) or (route.factory is not None):
                logger.info(fmt % (route.name, pattern, '<unknown>'))
            else:
                view_callable = registry.adapters.lookup(
                    (IViewClassifier, request_iface, Interface),
                    IView, name='', default=None)
                logger.info(fmt % (route.name, pattern, view_callable))
    logger.debug("ok.")
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 8080, app)
    logger.info("port: %s", 8080)
    server.serve_forever()
