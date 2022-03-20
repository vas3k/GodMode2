import os

from werkzeug.middleware.proxy_fix import ProxyFix

import settings
from godmode import logging
from godmode.app import create_app
from models.index import IndexAdminModel
from models.vas3k_365 import The365AdminModel
from models.vas3k_comments import CommentAdminModel
from models.vas3k_stories import StoryAdminModel
from models.vas3k_stories_en import StoryENAdminModel
from models.vas3k_subscribers import SubscriberAdminModel

log = logging.getLogger(__name__)

app = create_app(
    models=[
        IndexAdminModel,
        StoryAdminModel,
        CommentAdminModel,
        The365AdminModel,
        StoryENAdminModel,
        SubscriberAdminModel,
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
