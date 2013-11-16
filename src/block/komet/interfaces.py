# -*- coding:utf-8 -*-
from zope.interface import Interface

class IWalking(Interface):
    def __call__(target):
        pass

class IFolding(Interface):
    def __call__(template_itr, val_store, default, callback):
        pass

class IProducing(Interface):
    def __call__(template, params):
        pass

class IParsing(Interface):
    def __call__(subject):
        pass

class IValidating(Interface):
    def __call__(subject):
        pass

class IRegistering(Interface):
    def register(name, **kwargs):
        pass


class IMapping(Interface):
    def __call__(target):
        pass

class ITarget(Interface):
    pass

## types
class IType(Interface):
    pass
class IUnknown(IType):
    pass
class IBytes(IType):
    pass
class IString(IType):
    pass
class IBoolean(IType):
    pass
class INothing(IType):
    pass
class IInteger(IType):
    pass
class IFloat(IType):
    pass
class IDateTime(IType):
    pass
class IDate(IType):
    pass
class ITime(IType):
    pass
