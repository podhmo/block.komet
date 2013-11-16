# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from ..interfaces import IProducing

@implementer(IProducing)
class ModelProducing(object):
    def __init__(self, session_factory, Model):
        self.session_factory = session_factory
        self.Model = Model

    def get(self, id_):
        session = self.session_factory()
        return session.query(self.Model).get(id_)

    def list(self, query_params):
        session = self.session_factory()
        return session.query(self.Model)
