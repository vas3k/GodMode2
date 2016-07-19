import logging
import sys
from collections import defaultdict
from urllib.parse import urlencode

from flask import Flask, g, request
from raven.contrib.flask import Sentry

import settings
from common.acl import ACL
from common.exceptions import GodModeException, AuthFailed, BadParams
from db.godmode import GodModeDatabase
from models.godmode_auth import GodModeAuthAdminModel
from models.godmode_log import GodModeLogAdminModel
from models.godmode_policies import GodModePoliciesAdminModel
from models.godmode_sessions import GodModeSessionsAdminModel
from models.godmode_users import GodModeUsersAdminModel

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(settings.APP_CODE)
sentry = Sentry()

internal_model_classes = [
    GodModeUsersAdminModel,
    GodModeAuthAdminModel,
    GodModeSessionsAdminModel,
    GodModePoliciesAdminModel,
    GodModeLogAdminModel
]


class GodModeApp:
    def __init__(self, databases, models):
        self.databases = [GodModeDatabase()] + [db() for db in databases]
        self.flask = Flask(settings.APP_CODE)
        self.init_sentry()
        self.models, self.models_map = self.init_models(models)
        self.init_flask()
        self.load_template_filters()
        if settings.DEBUG:
            self.debug()

    def __call__(self, environ, start_response):
        return self.flask.wsgi_app(environ, start_response)

    def init_flask(self):
        self.flask.register_error_handler(GodModeException, lambda error: error.handler())

        @self.flask.before_request
        def before_request():
            g.db = {}
            g.db_session = {}
            for db in self.databases:
                g.db[db.__class__.__name__] = db.engine.connect()
                g.db_session[db.__class__.__name__] = db.session()

        @self.flask.teardown_request
        def after_request(exc):
            for key, connection in g.db.items():
                connection.close()

            for key, session in g.db_session.items():
                session.commit()
                session.close()

        @self.flask.before_request
        def check_user_auth():
            try:
                g.user = GodModeUsersAdminModel.user(request)
            except (BadParams, AuthFailed):
                g.user = None

    def init_sentry(self):
        if not settings.DEBUG and settings.SENTRY_DSN:
            sentry.init_app(self.flask, dsn=settings.SENTRY_DSN)

    def init_models(self, model_classes):
        models = []
        models_map = {}
        for model_class in internal_model_classes + model_classes:
            model = model_class(app=self)
            models.append(model)
            if hasattr(model, "db") and hasattr(model, "table") and model.table:
                if hasattr(model.table, "__tablename__"):
                    models_map["%s_%s" % (model.db.__name__, model.table.__tablename__)] = model
                elif hasattr(model.table, "__table__"):
                    models_map["%s_%s" % (model.db.__name__, model.table.__table__.name)] = model
        return models, models_map

    def load_template_filters(self):
        @self.flask.template_filter("group_models")
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

        @self.flask.template_filter("no_exception")
        def no_exception(item, default=""):
            try:
                return str(item)
            except ValueError:
                return default

        @self.flask.template_global("magic_params")
        def magic_params(request, key, value):
            params = dict(request.args or {})  # because of read-only
            if value:
                params.update({key: value})
            elif key in params.keys():
                del params[key]
            return "{}?{}".format(request.path, urlencode(params)) if params else request.path

        @self.flask.context_processor
        def godmode_context_processor():
            return dict(me=g.user, ACL=ACL, settings=settings)

    def gmlog(self, model=None, ids=None, action=None, details=None, reason=None):
        session = g.db_session[GodModeDatabase.__name__]
        item = GodModeLogAdminModel.table(**{
            "user": g.user.login,
            "model": str(model)[:64],
            "action": str(action)[:512],
            "ids": str(ids)[:512],
            "details": str(details)[:512],
            "reason": reason
        })
        session.add(item)
        session.commit()
        return item

    def debug(self):
        log.info("Models: %s" % self.models)
        log.info("Databases: %s" % self.databases)
        log.info("URLs: %s" % self.flask.url_map)

    def run(self):
        log.info("GodMode is running...")
        self.flask.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
