# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer
from .interfaces import IRequestParsing

@implementer(IRequestParsing)
class OneModelParsing(object):
    def __init__(self, get_dict, id_name="id"):
        self.id_name = id_name
        self.get_dict = get_dict

    def __call__(self, request):
        return self.get_dict(request)[self.id_name]
