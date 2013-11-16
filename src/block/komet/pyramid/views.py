# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from zope.interface import directlyProvides
from pyramid.httpexceptions import HTTPNotFound

from block.komet.exceptions import (
    CreationFailure,
    UpdatingFailure,
    DelitingFailure,
    ValidationFailure
)

from .interfaces import (
    ICreating,
    IUpdating,
    IDeleting,
)

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
        directlyProvides(request, ICreating)
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                params = self.parsing(request)
                target = context.try_commit(self.parsing, params, context.producing.create)
                return {"status": True, "message": "created", "data": context.walking(target)}
            except (CreationFailure, ValidationFailure) as e:
                return {"status": False, "message": repr(e), "data": dict(params)}

class OneModelUpdatingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        directlyProvides(request, IUpdating)
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                id_, params = self.parsing(request)
                commit = lambda params: context.producing.update(id_, params)
                target = context.try_commit(self.parsing, params, commit, id=id_)
                return {"status": True, "message": "updated", "data": context.walking(target)}
            except (UpdatingFailure, ValidationFailure) as e:
                return {"status": False, "message": repr(e), "data": dict(params)}


class OneModelDeletingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        directlyProvides(request, IDeleting)
        with context.try_maybe_notfound(HTTPNotFound):
            try:
                params = self.parsing(request)
                context.try_commit(self.parsing, params, context.producing.delete)
                return {"status": True, "message": "deleted", "data": {}}
            except (DelitingFailure , ValidationFailure) as e:
                return {"status": False, "message": repr(e), "data": dict(params)}

class OneModelListingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        targets = context.producing.list(self.parsing(request))
        walking = context.walking
        return {"status": True, "data": [walking(t) for t in targets]}
