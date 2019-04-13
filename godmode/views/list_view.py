from flask import request, render_template, g
from sqlalchemy import exc, text

from godmode import logging
from godmode.views.view import BaseView
from godmode.api import API, join_url

log = logging.getLogger(__name__)


class BaseListView(BaseView):
    title = "List"
    name = "list"
    layout = "table"
    template = "list.html"
    fields = []
    display = []
    sorting = None
    batch_actions = []
    object_actions = []
    max_per_page = 100
    has_list_delete = True
    default_sorting = text("id desc")

    max_offset = {}
    max_limit = {}

    def __init__(self, model, app):
        super().__init__(model, app)
        self.acl = model.acl
        if self.sorting is None:
            self.sorting = self.all_columns

    def init_actions(self):
        super().init_actions()
        if self.batch_actions:
            self.batch_actions_obj = []
            for action in self.batch_actions or []:
                action_object = action(app=self.app, model=self.model, view=self)
                self.app.add_url_rule(
                    rule=join_url([self.model.url_prefix, self.model.name, "batch", action.name]),
                    endpoint="{}_{}_{}".format(self.__class__.__name__, "batch", action.__name__),
                    view_func=action_object.dispatch_request
                )
                self.batch_actions_obj.append(action_object)

        if self.object_actions:
            self.object_actions_obj = []
            for action in self.object_actions or []:
                action_object = action(app=self.app, model=self.model, view=self)
                self.app.add_url_rule(
                    rule=join_url([self.model.url_prefix, self.model.name, "<id>", action.name]),
                    endpoint="{}_{}_{}".format(self.__class__.__name__, "object", action.__name__),
                    view_func=action_object.dispatch_request
                )
                self.object_actions_obj.append(action_object)

    def get(self):
        filters = API.get_str(request, "filters", required=False)
        order_by = API.get_str(request, "order_by", required=False)
        if not order_by:
            if self.default_sorting is not None:
                order_by = self.default_sorting
            else:
                order_by = self.sorting[0]

        limit = API.get_int(request, "limit", required=False) or self.max_per_page
        offset = API.get_int(request, "offset", required=False) or 0

        max_offset = self.max_offset.get(g.user.acl, offset)
        max_limit = self.max_limit.get(g.user.acl, limit)

        if offset > max_offset:
            offset = max_offset

        if limit > max_limit:
            limit = max_limit

        try:
            raw_rows = self.model.list(
                filters=filters,
                sort_by=order_by,
                limit=limit or self.max_per_page,
                offset=offset or 0
            )
        except exc.SQLAlchemyError as error:
            message = error.orig if hasattr(error, "orig") else str(error)
            return render_template("error.html", message="Error: {}".format(message), filter_error=True)
        
        return self.render(
            rows=raw_rows,
            filters=filters,
            order_by=order_by,
            limit=limit,
            offset=offset
        )

    def row_class(self, row):
        return ""
