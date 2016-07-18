import glob
import logging
import os
import sys
from collections import defaultdict

from flask import Flask, g, request
from raven.contrib.flask import Sentry

import settings
from base.model import BaseAdminModel
from common.acl import ACL
from common.exceptions import GodModeException, AuthFailed, BadParams
from models.godmode_log import GodModeLogAdminModel
from models.godmode_users import GodModeUsersAdminModel
from tables.godmode import GodModeDatabase

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(settings.APP_CODE)
sentry = Sentry()


class GodModeApp(object):
    def __init__(self, databases=None):
        self.databases = [GodModeDatabase()] + [db() for db in databases]
        self.flask = Flask(settings.APP_CODE)
        self.init_sentry()
        self.models, self.models_map = self.load_models()
        self.initialize_flask()
        self.load_template_filters()
        self.debug()

    def __call__(self, environ, start_response):
        return self.flask.wsgi_app(environ, start_response)

    def initialize_flask(self):
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
            sentry.init_app(
                    self.flask,
                    dsn=settings.SENTRY_DSN
            )

    def load_models(self):
        models = []
        models_map = {}
        for name, admin in self.__classes_in_directory("models", base=BaseAdminModel):
            model = admin(app=self)
            models.append(model)
            if hasattr(model, "db") and hasattr(model, "table") and model.table:
                if hasattr(model.table, "__tablename__"):
                    models_map["%s_%s" % (model.db.__name__, model.table.__tablename__)] = model
                elif hasattr(model.table, "__table__"):
                    models_map["%s_%s" % (model.db.__name__, model.table.__table__.name)] = model
        return models, models_map

    @staticmethod
    def __classes_in_directory(directory, base):
        already_known = set()
        generated_path = os.path.join(os.path.dirname(__file__), directory)
        for filename in glob.glob("%s/*.py" % generated_path):
            with open(filename, "r", encoding="utf-8") as source_file:
                source = source_file.read()
            code = compile(source, filename, 'exec')
            namespace = {}
            exec(code, namespace)
            for name, klass in namespace.items():
                if isinstance(klass, type) and klass != base and base in klass.__bases__ and klass not in already_known:
                    already_known.add(klass)
                    yield name, klass

    def load_template_filters(self):
        @self.flask.template_filter("group_models")
        def group_models(models):
            groups = defaultdict(list)
            group_positions = defaultdict(lambda: 0)
            for model in models:
                if model.group is None:
                    group_positions[None] = 999999
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
            params = dict([(k, v) for k, v in request.args.items()])
            if value:
                params.update({key: value})
            else:
                if key in params.keys():
                    del params[key]

            if params:
                return "%s?" % request.path + "&".join(["%s=%s" % (k, v) for k, v in params.items()])
            else:
                return "%s" % request.path

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
        log.info("Running...")
        self.flask.run("localhost", 1488, debug=True)
