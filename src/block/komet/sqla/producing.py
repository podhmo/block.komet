# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from ..interfaces import IProducing

@implementer(IProducing)
class ModelProducing(object):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __call__(self, Model, id_):
        session = self.session_factory()
        return session.query(Model).get(id_)
