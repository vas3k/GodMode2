from flask import g, request, Flask

from godmode.exceptions import BadParams, AuthFailed
from godmode.models.godmode_users import GodModeUsersAdminModel


def before_request_middleware(app: Flask):
    app.before_request_funcs.setdefault(None, [
        add_user_to_request,
    ])


def add_user_to_request():
    try:
        g.user = GodModeUsersAdminModel.user(request)
    except (BadParams, AuthFailed):
        g.user = None
