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


class BadData(Exception):
    pass

class ValidationFailure(Exception):
    def __init__(self, message, original):
        self.message = message
        self.original = original

    def __str__(self):
        return self.message
