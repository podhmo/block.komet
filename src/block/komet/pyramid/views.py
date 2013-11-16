# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from block.komet.exceptions import CreationFailure
from block.komet.exceptions import UpdatingFailure
from block.komet.exceptions import DelitingFailure

class OneModelViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        target = context.producing.get(self.parsing(request))
        return {"status": True, "data": context.walking(target)}

class OneModelCreationViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        try:
            params = self.parsing(request)
            target = context.producing.create(params)
            return {"status": True, "message": "created", "data": context.walking(target)}
        except CreationFailure as e:
            return {"status": False, "message": repr(e), "data": params}

class OneModelUpdatingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        try:
            pair = self.parsing(request)
            target = context.producing.update(*pair)
            return {"status": True, "message": "updated", "data": context.walking(target)}
        except UpdatingFailure as e:
            return {"status": False, "message": repr(e), "data": pair}


class OneModelDeletingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        try:
            params = self.parsing(request)
            context.producing.delete(params)
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
