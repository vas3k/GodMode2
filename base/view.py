import logging

from flask import g, redirect, render_template
from flask.views import MethodView

import settings
from common.acl import ACL
from common.api import join_url
from common.exceptions import AccessDenied
from widgets.factory import WidgetFactory

log = logging.getLogger(settings.APP_CODE)


class BaseView(MethodView):
    app = None
    model = None
    url = None
    name = None
    title = "Base view"
    template = "blank.html"
    acl = ACL.ALL
    policy = None
    actions = []
    fields = []
    display = []
    custom_widgets = {}

    def __init__(self, model, app):
        log.info("Init view: {}".format(self.__class__.__name__))
        self.app = app
        self.model = model
        self.policy = "{}.{}".format(self.model.policy, self.name)
        self.fields_obj = []
        self.widgets = {}
        self.all_columns_with_metadata = []
        self.all_columns = []
        self.actions_obj = []
        self.custom_widgets = self.custom_widgets or self.model.custom_widgets
        self.init_actions()
        if self.model.table is not None:
            self.init_fields()

    def init_fields(self):
        self.all_columns_with_metadata = self.model.table.__table__.columns
        self.all_columns = [column.name for column in self.all_columns_with_metadata]
        self.fields = list(self.fields or self.model.fields or self.all_columns or [])
        self.display = list(self.display or self.model.display or [])
        populate_display_with_fields = not self.display

        self.fields_obj = []
        self.widgets = {}
        for field in self.fields:
            field_options = {}
            if isinstance(field, list) or isinstance(field, tuple):
                field_name, field_options = field
            else:
                field_name = field

            field_options = dict(field_options)

            column_with_metadata = None
            for column_with_metadata in self.all_columns_with_metadata:
                if column_with_metadata.name == field_name:
                    break

            if column_with_metadata is None and field_options.get("widget") is None:
                raise Exception("No column named '{}' in table metadata, specify a widget!".format(field_name))

            if field_options.get("widget"):
                column_widget = field_options["widget"](field_name, meta=column_with_metadata, model=self.model)
            elif field_name in self.custom_widgets:
                column_widget = self.custom_widgets[field_name](field_name, meta=column_with_metadata, model=self.model)
            else:
                column_widget = WidgetFactory.build(field_name, meta=column_with_metadata, model=self.model)

            field_options["widget"] = column_widget
            field_options["meta"] = column_with_metadata
            field_options["filterable"] = column_widget.filterable

            if populate_display_with_fields:
                self.display.append(field_name)
            self.fields_obj.append((field_name, field_options))
            self.widgets[field_name] = column_widget

    def init_actions(self):
        if self.actions:
            self.actions_obj = []
            for action in self.actions or []:
                action_object = action(app=self.app, model=self.model, view=self)
                self.app.flask.add_url_rule(
                        rule=join_url([self.model.url_prefix, self.model.name, "<id>", action.name]),
                        endpoint="{}_{}".format(self.__class__.__name__, action.__name__),
                        view_func=action_object.dispatch_request,
                        methods=action_object.methods
                )
                self.actions_obj.append(action_object)

    def render(self, **context):
        context.update({
            "app": self.app,
            "model": self.model,
            "view": self
        })
        return render_template(self.template, **context)

    def dispatch_request(self, *args, **kwargs):
        if self.acl != ACL.OPEN and not g.user:
            return redirect("/login/")

        if not ACL.has_access(g.user, self):
            raise AccessDenied(message="Looks like you cannot view this page.")

        return super().dispatch_request(*args, **kwargs)
