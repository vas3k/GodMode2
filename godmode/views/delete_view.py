from flask import redirect

from godmode.views.view import BaseView
from godmode.acl import ACL


class BaseDeleteView(BaseView):
    title = "Delete"
    name = "delete"
    acl = ACL.ADMIN

    def get(self, item_id):
        self.model.delete(id=item_id)
        return redirect("{}{}".format(self.model.url_prefix, self.model.name))
