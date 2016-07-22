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
            return self.render()

    list_view = DemoIndexView
