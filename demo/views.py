# -*- coding:utf-8 -*-


def get(context, request):
    context.query.filter_by(id=request.matchdict["id"]).register()
    return {
        "target": mapping(ITarget)
    }
