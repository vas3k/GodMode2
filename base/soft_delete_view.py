from flask import redirect

from base.view import BaseView
from common.acl import ACL


class BaseSoftDeleteView(BaseView):
    title = "Soft Delete"
    name = "soft_delete"
    acl = ACL.ADMIN

    def get(self, id):
        self.model.soft_delete(id=id)
        return redirect("{}{}".format(self.model.url_prefix, self.model.name))
