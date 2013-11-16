# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from block.komet.exceptions import (
    CreationFailure,
    UpdatingFailure,
    DelitingFailure,
)

from pyramid.httpexceptions import HTTPNotFound
class OneModelViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        with context.try_maybe_notfound(HTTPNotFound):
            target = context.producing.get(self.parsing(request))
            return {"status": True, "data": context.walking(target)}


class OneModelCreationViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                params = self.parsing(request)
                target = context.try_commit(self.parsing, params, context.producing.create)
                return {"status": True, "message": "created", "data": context.walking(target)}
            except CreationFailure as e:
                return {"status": False, "message": repr(e), "data": params}

class OneModelUpdatingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                id_, params = self.parsing(request)
                commit = lambda params: context.producing.update(id_, params)
                target = context.try_commit(self.parsing, params, commit)
                return {"status": True, "message": "updated", "data": context.walking(target)}
            except UpdatingFailure as e:
                return {"status": False, "message": repr(e), "data": params}


class OneModelDeletingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                params = self.parsing(request)
                context.try_commit(self.parsing, params, context.producing.delete)
                return {"status": True, "message": "deleted", "data": {}}
            except DelitingFailure as e:
                return {"status": False, "message": repr(e), "data": params}

class OneModelListingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        targets = context.producing.list(self.parsing(request))
        walking = context.walking
        return {"status": True, "data": [walking(t) for t in targets]}
