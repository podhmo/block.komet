# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

## todo: refine
class CreationFailure(Exception):
    pass
class UpdatingFailure(Exception):
    pass
class DelitingFailure(Exception):
    pass
class NotFoundFailure(Exception):
    pass
