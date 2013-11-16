# -*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Session = orm.sessionmaker()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    name = sa.Column(sa.String(255), unique=True, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.now, default=datetime.now)

from pyramid.config import Configurator

def setup_database(config):
    # engine = sa.create_engine('sqlite://', echo=True)
    engine = sa.create_engine('sqlite://')
    Session.configure(bind=engine, autoflush=False)
    Base.metadata.bind = engine
    Base.metadata.create_all()


    session = Session()
    session.add(User(name="foo"))
    session.add(User(name="boo"))
    session.add(User(name="bar"))
    session.commit()

def session_factory(request):
    try:
        return request.session
    except AttributeError:
        v = request.session = Session()
        return v

def setup_views(config):
    from block.komet.mapping import (
        get_mapping_function_factory
    )
    mapping = get_mapping_function_factory(config, name="python")
    installer = config.maybe_dotted("block.komet.pyramid.examples.sqla.install_komet_resource")
    komet_resource_factory = installer(config, session_factory, mapping, name="komet")
    builder = config.view_registering_builder(komet_resource_factory)
    vcs = builder.view_category_set
    config.maybe_dotted("block.komet.pyramid.examples.sqla.detail_view_category")(vcs)
    config.maybe_dotted("block.komet.pyramid.examples.sqla.list_view_category")(vcs)
    builder.build(config, User)

def simple_commit_tween(handler, registry): #todo:fix
    def tween(request):
        response = handler(request)
        request.session.commit()
        return response
    return tween

def main(global_config, prefix="demo.main.", **settings):
    config = Configurator(settings=settings)
    config.include("block.komet.mapping.install_python_mapping")
    config.include("block.komet.pyramid.registering")
    config.include("block.komet.pyramid.resources")
    config.include(setup_database)
    config.include(setup_views)
    ## buggy
    config.add_tween("{prefix}simple_commit_tween".format(prefix=prefix))
    config.commit()
    from block.komet.pyramid.tools import proutes
    proutes(config)
    logger.debug("ok.")
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({}, prefix=".")
    server = make_server('0.0.0.0', 8080, app)
    logger.info("port: %s", 8080)
    server.serve_forever()

"""
curl http://localhost:8080/api/users
curl -d name="barr" http://localhost:8080/api/users
curl http://localhost:8080/api/users/3
curl -d name="fixed" http://localhost:8080/api/users/3
curl -X DELETE http://localhost:8080/api/users/3
"""
