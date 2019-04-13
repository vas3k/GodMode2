from flask import g
from sqlalchemy.exc import DataError

from godmode.models.base import BaseAdminModel
from godmode.views.view import BaseView
from godmode.acl import ACL
from database.demo import demo_database


class IndexAdminModel(BaseAdminModel):
    acl = ACL.ALL
    db = demo_database
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
                total_users = session.execute("select count(id) as value from users").first()[0]
            except DataError:
                total_users = 0

            try:
                total_posts = session.execute("select count(id) as value from posts").first()[0]
            except DataError:
                total_posts = 0

            context = {
                "message": "Welcome to GodMode, {}. You can customize this page.".format(g.user.login),
                "total_users": total_users,
                "total_posts": total_posts
            }
            return self.render(**context)

    list_view = DemoIndexView
