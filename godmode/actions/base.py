import json

from flask import g, request, render_template
from flask.views import View

from godmode import logging
from godmode.acl import ACL
from godmode.audit_log import audit_log
from godmode.exceptions import AccessDenied

log = logging.getLogger(__name__)


class BaseAction(View):
    name = None
    title = None
    acl = ACL.ADMIN
    enable_log = True
    style = ""
    policy = None
    stay_on_page = False
    item_limit = None

    def __init__(self, app, model=None, view=None):
        log.info("Init action: {}".format(self.__class__.__name__))
        self.app = app
        self.model = model
        self.view = view
        self.policy = "{}.{}".format(self.view.policy, self.name)
        log.info(self.policy)

    def url(self):
        return

    def dispatch_request(self, *args, **kwargs):
        has_access = ACL.has_access(g.user, self)
        if not has_access:
            raise AccessDenied(message="You don't have an access to this page.")

        audit_log(
            user=g.user,
            model=self.model,
            ids=kwargs.get("id") or request.args.get("ids"),
            action=self.name
        )

        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        item_id = kwargs.get("id", None)
        if item_id:
            return self.do_item_action(*args, **kwargs)

        ids = request.args.get("ids")
        if not ids:
            return json.dumps({
                "remove_rows": False
            })

        id_list = ids.split(",")

        if self.item_limit:
            id_list = id_list[:self.item_limit]

        for item_id in id_list:
            try:
                item_id = int(item_id)
            except (ValueError, TypeError):
                continue
            kwargs["id"] = item_id
            self.do_item_action(*args, **kwargs)

        return json.dumps({
            "remove_rows": True
        })

    def render_form(self, *args, **kwargs):
        return render_template("actions/button_action.html", url=self.name, button_label="Submit")

    def do_item_action(self, *args, **kwargs):
        raise NotImplementedError()
