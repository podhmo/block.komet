# -*- coding:utf-8 -*-
from zope.interface import Interface
from ..interfaces import IRegistering
from ..interfaces import IParsing

class IResourceFactory(Interface):
    pass

class IRequestParsing(IParsing):
    def __call__(self, request):
        pass

class IViewCategorySetRegister(IRegistering):
    def __call__(config, Target):
        pass

class IViewCategoryRegister(IRegistering):
    def __call__(config, Target, resource):
        pass

class IViewRegister(IRegistering):
    def __call__(config, Target, route_name):
        pass
