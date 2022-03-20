from sqlalchemy.exc import DataError

from godmode.models.base import BaseAdminModel
from godmode.views.view import BaseView
from godmode.acl import ACL
from database.vas3kru import vas3k_database


class IndexAdminModel(BaseAdminModel):
    acl = ACL.ALL
    db = vas3k_database
    title = "Home"
    place = None
    url_prefix = "/"

    class DemoIndexView(BaseView):
        acl = ACL.ALL
        url = "/"
        title = "Index"
        template = "index.html"

        def get(self):
            session = self.model.session

            try:
                subscribers = session.execute("select count(*) as cnt from subscribers where is_confirmed = true").first()
                subscribers = subscribers[0] if subscribers else 0
            except DataError:
                subscribers = 0

            context = {
                "newsletter_subscribers": subscribers
            }

            return self.render(**context)

    list_view = DemoIndexView
