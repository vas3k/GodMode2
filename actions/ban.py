from flask import render_template

from base.action import BaseAction
from common.acl import ACL


class BanAction(BaseAction):
    name = "ban"
    title = "Ban"
    acl = ACL.ADMIN
    stay_on_page = True
    style = "white-space: nowrap;"
    methods = ["GET", "POST"]

    def do_item_action(self, *args, **kwargs):
        id = kwargs.pop("id")
        self.model.update(id=id, is_locked=True)
        return render_template("success.html", message="User {} was banned".format(id))
