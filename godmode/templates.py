from collections import defaultdict
from urllib.parse import urlencode

from flask import g, Flask

import settings
from godmode.acl import ACL
from godmode.models import models, model_map, model_hash


def init_templates(app: Flask):
    app.context_processor(godmode_context_processor)
    app.add_template_filter(no_exception, "no_exception")
    app.add_template_global(model_hash, "model_hash")
    app.add_template_global(magic_params, "magic_params")


def godmode_context_processor():
    return dict(
        me=g.user,
        sidebar_models=group_models(models),
        navbar_models=[m for m in models if m.place == "navbar"],
        model_map=model_map,
        ACL=ACL,
        settings=settings
    )


def group_models(models):
    groups = defaultdict(list)
    group_positions = defaultdict(lambda: 0)
    for model in models:
        if model.group is None:
            group_positions[None] = 9999999
            groups[None].append(model)
            continue

        group_positions[model.group] = model.group.index
        groups[model.group].append(model)

    return [(name, sorted(groups[name], key=lambda model: model.index, reverse=True)) for name, index in
            sorted(group_positions.items(), key=lambda items: items[1], reverse=True)]


def no_exception(item, default=""):
    try:
        return str(item)
    except ValueError:
        return default


def magic_params(request, key, value):
    params = request.args.to_dict(flat=True)
    if value:
        params.update({key: value})
    elif key in params.keys():
        del params[key]
    return "{}?{}".format(request.path, urlencode(params)) if params else request.path
