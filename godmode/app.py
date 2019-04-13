from typing import List, Any

from flask import Flask

import settings
from godmode import logging
from godmode.exceptions import GodModeException
from godmode.middlewares.after_request import after_request_middleware
from godmode.middlewares.before_request import before_request_middleware
from godmode.middlewares.teardown_appcontext import teardown_appcontext_middleware
from godmode.models import init_models, init_internal_models
from godmode.templates import init_templates

log = logging.getLogger(__name__)


def create_app(
        models: List[Any]
) -> Flask:

    log.debug("Loading Flask application...")
    app = Flask(__name__, root_path=settings.BASE_PATH)

    app.register_error_handler(
        GodModeException,
        lambda error: error.handler()
    )

    log.debug("Loading middlewares...")
    before_request_middleware(app)
    after_request_middleware(app)
    teardown_appcontext_middleware(app)

    log.debug("Loading templates...")
    init_templates(app)

    log.debug("Loading admin models...")
    init_internal_models(app)
    init_models(app, models)

    return app
