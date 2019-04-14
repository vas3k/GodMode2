import os

from werkzeug.middleware.proxy_fix import ProxyFix

import settings
from godmode import logging
from godmode.app import create_app
from models.index import IndexAdminModel
from models.demo_posts import PostsAdminModel
from models.demo_retention import RetentionAdminModel
from models.demo_users import UsersAdminModel

log = logging.getLogger(__name__)

app = create_app(
    models=[
        IndexAdminModel,
        PostsAdminModel,
        UsersAdminModel,
        RetentionAdminModel
    ]
)

wsgi = ProxyFix(app.wsgi_app)

if __name__ == '__main__' and not os.environ.get("TRAVIS"):
    log.info("GodMode is starting...")
    app.run(
        debug=settings.DEBUG,
        host=settings.APP_HOST,
        port=settings.APP_PORT
    )
