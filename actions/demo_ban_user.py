from flask import render_template

from godmode.actions.base import BaseAction
from godmode.acl import ACL


class DemoBanUserAction(BaseAction):
    name = "ban"
    title = "Ban"
    acl = ACL.ADMIN
    stay_on_page = True
    style = "white-space: nowrap;"
    methods = ["GET", "POST"]

    def do_item_action(self, *args, **kwargs):
        user_id = kwargs.pop("id")
        self.model.update(id=user_id, is_locked=True)
        return render_template("success.html", message="User {} was banned".format(id))
