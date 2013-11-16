# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class OneModelViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        target = context.producing.get(self.parsing(request))
        return context.walking(target)

class ListingViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        targets = context.producing.list(self.parsing(request))
        walking = context.walking
        return [walking(t) for t in targets]
