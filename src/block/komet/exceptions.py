# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from zope.interface import implementer
from .interfaces import IFailure, IHasMessage
from block.form.validation import ValidationError

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

ValidationFailure = implementer(IFailure)(ValidationError)

@implementer(IFailure)
class NotFoundFailure(Exception):
    pass

@implementer(IFailure)
class BadData(Exception):
    pass
