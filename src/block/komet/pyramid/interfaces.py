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


## validation
class IValidationGenerator(Interface):
    def __call__(request, kwargs):
        pass

class IDataValidation(Interface):
    def __call__(request, data, errors, **kwargs):
        pass

## stage
class ICreating(Interface):
    pass
class IDeleting(Interface):
    pass
class IUpdating(Interface):
    pass
