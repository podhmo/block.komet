# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)

class OneModelViewFactory(object):
    def __init__(self, parsing):
        self.parsing = parsing

    def __call__(self, context, request):
        target = context.producing(self.parsing(request))
        return context.walking(target)
