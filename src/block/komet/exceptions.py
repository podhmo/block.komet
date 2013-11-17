# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from zope.interface import implementer
from .interfaces import IFailure, IHasMessage

## todo: refine
@implementer(IFailure)
class CreationFailure(Exception):
    pass
@implementer(IFailure)
class UpdatingFailure(Exception):
    pass
@implementer(IFailure)
class DelitingFailure(Exception):
    pass
@implementer(IFailure)
class NotFoundFailure(Exception):
    pass

@implementer(IFailure)
class BadData(Exception):
    pass

@implementer(IHasMessage)
class ValidationFailure(Exception):
    def __init__(self, message, original):
        self.message = message
        self.original = original

    def __str__(self):
        return self.message
