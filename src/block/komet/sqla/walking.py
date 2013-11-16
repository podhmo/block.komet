# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from zope.interface import implementer

from collections import (
    OrderedDict, 
    namedtuple
)

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql.visitors import VisitableType
from ..interfaces import IWalking, IUnknown
from ..folding import flatten_folding

from .types import default_classfier

@implementer(IWalking)
class MapperWalking(object):
    def __init__(self, walking_template, mapping, create_store=OrderedDict):
        self.walking_template = walking_template
        self.create_store = create_store
        self.mapping = mapping
        self.opequeue_cache = {}

    def get_opequeue(self, k, template):
        try:
            return self.opequeue_cache[k]
        except KeyError:
            v = self.opequeue_cache[k] = template.compile(self.mapping)
            return v

    def __call__(self, target):
        template = self.walking_template(target) #xxx
        opequeue = self.get_opequeue(template.mapper, template)

        def callback(store, name, convert, val):
            store[name] = convert(val)
        return template.walk(self, target, opequeue, callback)


Operation = namedtuple("Operation", "name convert")

class ColumnsWalkingTemplate(object):
    def __init__(self, target, type_classifier=default_classfier):
        self.mapper = inspect(target).mapper
        self.folding = flatten_folding
        self.type_classifier = type_classifier

    def compile(self, mapping):
        opequeue = []
        for prop in self.mapper.attrs:
            if isinstance(prop, ColumnProperty):
                types_list = tuple((c.type.__class__ if type(c.type) != VisitableType else c.type)
                                   for c in prop.columns)
                iface = self.type_of(types_list)
                # logger.debug("*types_list={types_list}, iface={iface}".format(types_list=types_list, iface=iface))
                if iface is IUnknown:
                    logger.warn("*IUnknown found. ignored")
                    continue
                mapping_function = mapping(iface)
                def convert(val, name=prop.key, mapping=mapping_function):
                    return mapping(getattr(val, name))
                opequeue.append(Operation(prop.key, convert))
        return opequeue

    def walk(self, walking, target, opequeue, callback):
        store = walking.create_store()
        flatten_folding(opequeue, target, store, callback)
        return store

    def type_of(self, fields):
        try:
            return self.type_classifier[fields]
        except KeyError:
            logger.warn("*type not found %s", fields)
            return IUnknown
