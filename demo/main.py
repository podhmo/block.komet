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
    return Session() #buggy

def setup_resource_factory(config):
    from block.komet.sqla import (
        MapperWalking, 
        ColumnsWalkingTemplate, 
        ModelProducing
    )
    from block.komet.mapping import (
        get_mapping_function_factory
    )
    from block.komet.pyramid.resources import (
        KometResourceFactory
    )
    json_mapping = get_mapping_function_factory(config, name="json")
    walking = MapperWalking(ColumnsWalkingTemplate, json_mapping)
    producing = ModelProducing(session_factory)
    config.register_resource_factory(KometResourceFactory(producing, walking))

def setup_views(config):
    from block.komet.pyramid.views import (
        OneModelViewFactory
    )
    resource_factory = config.get_resource_factory()
    builder = config.view_registering_builder(resource_factory)
    vcs = builder.view_category_set
    def pattern_fn(Model):
        return "/{}/{{id}}".format(Model.__name__.lower())

    def route_name_fn(Model):
        return "{}.detail".format(Model.__name__.lower())
    with vcs.view_category(pattern_fn, route_name_fn) as vc:
        def parsing(request):
            return request.matchdict["id"]
        vc.view(OneModelViewFactory(parsing), request_method="GET", renderer="json")
    builder.build(config, User)

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("block.komet.mapping.install_json_mapping")
    config.include("block.komet.pyramid.registering")
    config.include("block.komet.pyramid.resources")
    config.include(setup_database)
    config.include(setup_resource_factory)
    config.include(setup_views)
    config.commit()
    from block.komet.pyramid.tools import proutes
    proutes(config)
    logger.debug("ok.")
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 8080, app)
    logger.info("port: %s", 8080)
    server.serve_forever()
