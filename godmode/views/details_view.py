from flask import render_template

from godmode import logging
from godmode.views.view import BaseView
from godmode.acl import ACL

log = logging.getLogger(__name__)


class BaseDetailsView(BaseView):
    title = "Details"
    name = "details"
    layout = "table"
    template = "details.html"
    fields = None
    display = None
    actions = []
    acl = ACL.ADMIN

    def get(self, id):
        item = self.model.get(id=id)
        if not item:
            return render_template("error.html", message="'{}' does not exist.".format(self.model.name))
        return self.render(item=item)
