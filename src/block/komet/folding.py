# -*- coding:utf-8 -*-
from zope.interface import provider
from .interfaces import IFolding


@provider(IFolding)
def flatten_folding(template_itr, val_store, default, callback):
    for name, bound in template_itr:
        callback(default, name, bound, val_store)
    return default

