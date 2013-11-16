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

class ValidationFailure(Exception):
    def __init__(self, errors, original):
        self.errors = errors
        self.original = original

    @property
    def message(self):
        r = []
        for k, vs in self.errors:
            sr = "\t".join(vs)
            if sr:
                r.append(k)
                r.append("\t")
                r.extend(sr)
        return "\n".join(r)
