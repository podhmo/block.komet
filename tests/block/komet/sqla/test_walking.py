# -*- coding:utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
import unittest

from block.komet import testing

Session = orm.sessionmaker()
engine = sa.create_engine('sqlite://')
Session.configure(bind=engine, autoflush=False)

Base = declarative_base(bind=engine)

class Group(Base):
    __tablename__ = "groups"
    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    name = sa.Column(sa.String(255), unique=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    group_id = sa.Column(sa.Integer(), sa.ForeignKey("groups.id"))
    group = orm.relationship(Group, uselist=False, backref=("users"))
    name = sa.Column(sa.String(255), unique=True, nullable=False)

class LogMessage(Base):
    __tablename__ = "log_messags"
    id = sa.Column(sa.Integer(), primary_key=True, nullable=False)
    created_at = sa.Column(sa.DateTime())
    content = sa.Column(sa.Text())

class GroupUser(Base):
    __table__ = sa.join(Group.__table__, User.__table__)
    id = orm.column_property(Group.__table__.c.id, User.__table__.c.group_id)
    user_id = User.__table__.c.id
    group_name = Group.__table__.c.name


class WalkingTests(unittest.TestCase):
    def tearDown(self):
        testing.tearDown()
        Base.metadata.drop_all()

    def setUp(self):
        Base.metadata.create_all()
        self.config = testing.setUp()
        from block.komet.mapping import includeme
        self.config.include(includeme)

    def _getTarget(self):
        from block.komet.sqla import MapperWalking
        return MapperWalking

    def _makeOne(self, *args, **kwargs):
        from block.komet.mapping import get_mapping_function_factory
        mapping = get_mapping_function_factory(self.config, name="json")

        target = self._getTarget()
        from block.komet.sqla import ColumnsWalkingTemplate
        return target(ColumnsWalkingTemplate, mapping)

    def test_it__normal(self):
        user = User(id=1, name="foo")
        walker = self._makeOne()
        result = walker(user)
        expected = {"id": "1", "name": '"foo"', "group_id": "null"}
        self.assertEqual(dict(result), expected)


    def test_it__has_time(self):
        from datetime import datetime
        dt = datetime(2000, 1, 1, 1, 1)
        log = LogMessage(created_at=dt, content="initial commit")
        walker = self._makeOne()
        result = walker(log)
        expected = {'content': '"initial commit"',
                    'id': 'null',
                    'created_at': '2000-01-01T01:01:00'
                }
        self.assertEqual(dict(result), expected)

    def test_it__joined_mapper(self):
        user = GroupUser(name="foo", group_name="Group")
        walker = self._makeOne()
        result = walker(user)
        expected = {'group_name': '"Group"', 'user_id': 'null', 'id': 'null', 'name': '"foo"'}
        self.assertEqual(dict(result), expected)

    # def test_it__named_tuple(self):
    #     session = Session()
    #     group = Group(name="Group")
    #     user = User(name="foo", group=group)
    #     session.add(user)
    #     session.commit()

    #     session = Session()
    #     qs = session.query(User).join(Group).with_entities(Group.name, User.name)
    #     one = qs.first()
    #     walker = self._makeOne()
    #     result = walker(one)
        # self.assertEqual(dict(result), expected)
