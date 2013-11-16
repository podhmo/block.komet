# -*- coding:utf-8 -*-
from zope.interface import (
    Interface,
    Attribute
)
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

class IRegisterRepository(Interface):
    view_category_set = Attribute("")
    view_category = Attribute("")
    view = Attribute("")
