# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from ..interfaces import IProducing

@implementer(IProducing)
class ModelProducing(object):
    def __init__(self, session, Model):
        self.session = session
        self.Model = Model

    def get(self, id_):
        session = self.session
        return session.query(self.Model).get(id_)

    def create(self, params): #buggy
        session = self.session
        model = self.Model(**params)
        session.add(model)
        return model

    def update(self, id_, params): #buggy
        session = self.session
        model = self.get(id_)
        for k, v in params.items():
            setattr(model, k, v)
        session.add(model)
        return model

    def list(self, query_params):
        session = self.session
        return session.query(self.Model).filter_by(**query_params)
