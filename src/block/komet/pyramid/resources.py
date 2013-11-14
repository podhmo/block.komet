# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from pyramid.decorator import reify
from functools import partial

from zope.interface import implementer
from .interfaces import IResourceFactory

@implementer(IResourceFactory)
class KometResourceFactory(object):
    def __init__(self, producing, walking):
        self.producing = producing
        self.walking = walking

    def __call__(self, Model):
        return partial(KommetResource, self, Model)

class KommetResource(object):
    def __init__(self, env, Model, request):
        self.env = env
        self.Model = Model
        self.request = request

    @reify
    def producing(self):
        return partial(self.env.producing, self.Model)

    @reify
    def walking(self):
        return self.env.walking
