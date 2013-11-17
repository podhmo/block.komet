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
    from block.komet.pyramid.examples.sqla import (
        detail_view_category,
        list_view_category,
        install_komet_resource
    )
    mapping = get_mapping_function_factory(config, name="python")
    komet_resource_factory = install_komet_resource(config, session_factory, mapping, name="komet")

    builder = config.view_registering_builder("api", komet_resource_factory)
    vcs = builder.view_category_set
    detail_view_category(vcs, name="detail")
    list_view_category(vcs, name="list")

    ## todo:available options
    builder.build(config, User, {"list": {"list": {"query": {"order_by": "id desc"}}}})


def setup_validation_executor(config):
    from block.komet.pyramid.validation import ValidationExecuter
    def handle_request(request, kwargs):
        kwargs["session"] = request.context.session
        return kwargs
    def create_executor(vq):
        return ValidationExecuter(vq,
                                  handle_request=handle_request,
                                  CatchError=Exception)
    config.add_validation_executor(create_executor)

def setup_validations(config):
    from block.komet.pyramid.interfaces import ICreating, IUpdating
    from block.komet.pyramid.validation import ValidationQueue, with_pick

    class UniqueNameConflict(Exception):
        pass
    def unique_name_conflict(e):
        return "name: {} is conflict.".format(e.args[0])

    @with_pick(positionals=["session"], optionals=["id"])
    def unique_name(data, session, id=None):
        qs = session.query(User).filter_by(name=data["name"])
        if id:
            qs = qs.filter(User.id != id)
        if qs.count() > 0:
            raise UniqueNameConflict(data["name"])

    vq = ValidationQueue().add("name", unique_name)

    config.add_display_message(UniqueNameConflict, unique_name_conflict)
    config.add_validation([ICreating], User, vq)
    config.add_validation([IUpdating], User, vq)

def simple_commit_tween(handler, registry): #todo:fix
    def tween(request):
        response = handler(request)
        request.session.commit()
        return response
    return tween

def main(global_config, prefix="demo.main.", **settings):
    config = Configurator(settings=settings)
    config.include("block.komet.mapping.install_python_mapping")
    config.include("block.komet.pyramid")
    config.include(setup_database)
    config.include(setup_views)
    config.include(setup_validations)
    config.include(setup_validation_executor)
    ## buggy
    config.add_tween("{prefix}simple_commit_tween".format(prefix=prefix))
    config.scan(prefix.rstrip(".") if prefix != "." else ".")
    config.commit()
    from block.komet.pyramid.tools import proutes
    proutes(config)
    logger.debug("ok.")
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({}, prefix=".")

    session = Session()
    session.add(User(name="foo"))
    session.add(User(name="boo"))
    session.add(User(name="bar"))
    session.commit()

    server = make_server('0.0.0.0', 8080, app)
    logger.info("port: %s", 8080)
    server.serve_forever()

def tear_down():
    Base.metadata.drop_all()

"""
curl http://localhost:8080/api/users
curl -d name="barr" http://localhost:8080/api/users
curl http://localhost:8080/api/users/3
curl -d name="fixed" http://localhost:8080/api/users/3
curl -X DELETE http://localhost:8080/api/users/3
"""
