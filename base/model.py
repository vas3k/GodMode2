import copy
import logging

from flask import g
from sqlalchemy import text

import settings
from base.create_view import BaseCreateView
from base.delete_view import BaseDeleteView
from base.details_view import BaseDetailsView
from base.edit_view import BaseEditView
from base.list_view import BaseListView
from common.acl import ACL
from common.api import join_url

log = logging.getLogger(settings.APP_CODE)


class BaseAdminModel:
    app = None
    db = None
    table = None
    acl = ACL.ADMIN
    policy = None
    name = None
    title = None
    icon = "icon-loadingeight"
    index = 0
    url_prefix = "/models/"
    place = "sidebar"
    group = None
    actions = []
    batch_actions = []
    enable_log = True
    fields = None
    items = None
    display = None
    id_field = "id"
    widgets = {}
    excluded_fields_for_log = ["password", "pwd", "pass", "secret"]
    details_fields_on_delete = []

    views = {
        "list_view": "/",
        "edit_view": "/<id>/edit/",
        "create_view": "/create/",
        "details_view": "/<id>/details/",
        "delete_view": "/<id>/delete/",
        "soft_delete_view": "/<id>/soft_delete/"
    }

    list_view = BaseListView
    edit_view = BaseEditView
    create_view = BaseCreateView
    details_view = BaseDetailsView
    delete_view = BaseDeleteView

    def __init__(self, app):
        log.info("Init model: {}".format(self.__class__.__name__))
        self.app = app
        self.policy = "{}".format(self.name)
        self.init_views()

    def init_views(self):
        for view_name, view_url in self.views.items():
            view_class = getattr(self, view_name, None)
            if view_class is None:
                log.info("In {} view {} is undefined, skipped".format(self.__class__.__name__, view_name))
                setattr(self, "{}_obj".format(view_name), None)
                continue

            view_object = view_class(app=self.app, model=self)
            self.app.flask.add_url_rule(
                    rule=join_url([self.url_prefix, self.name, view_url]),
                    endpoint="{}_{}".format(self.__class__.__name__, view_class.__name__),
                    view_func=view_object.dispatch_request,
                    methods=view_object.methods
            )
            setattr(self, "{}_obj".format(view_name), view_object)

    @property
    def session(self):
        if not self.db:
            raise Exception("DB for admin {} is not initialized".format(self.__class__.__name__))

        try:
            return g.db_session[self.db.__name__]
        except KeyError as ex:
            raise Exception("No db to create session: %s" % ex)

    def list(self, filters, sort_by, limit=100, offset=0):
        items = self.session.query(self.table).order_by(sort_by)
        if filters:
            items = items.filter(text(filters))
        items = items.limit(limit).offset(offset)
        self.items = items
        items = ACL.filter_items(g.user, self)
        return items

    def get(self, **kwargs):
        item = self.session.query(self.table).filter_by(**kwargs).first()
        self.items = item
        item = ACL.filter_items(g.user, self)
        return item

    def delete(self, **kwargs):
        item = self.session.query(self.table).filter_by(**kwargs).first()
        self.items = item
        item = ACL.filter_items(g.user, self)
        self.before_delete(item)
        if not item:
            return

        if self.enable_log:
            details = None
            if self.details_fields_on_delete:
                details = ""
                for field_name in self.details_fields_on_delete:
                    field_value = getattr(item, field_name)
                    if field_value:
                        details = "{}, {}={}".format(details, field_name, field_value)
                details = details.lstrip(", ")
            self.app.gmlog(model=self.name, ids=item.id, action="delete", details=details)
        self.session.query(self.table).filter_by(**kwargs).delete(synchronize_session=False)
        self.session.commit()

    def soft_delete(self, **kwargs):
        item = self.session.query(self.table).filter_by(**kwargs).first()
        self.items = item
        item = ACL.filter_items(g.user, self)
        self.before_soft_delete(item)
        if item:
            if self.enable_log:
                self.app.gmlog(model=self.name, ids=item.id, action="soft_delete")
            self.soft_delete_action(item)

    def create(self, **kwargs):
        item = self.table(**kwargs)
        self.before_create(item)
        self.session.add(item)
        self.session.commit()
        self.after_create(item)
        if self.enable_log:
            self.app.gmlog(model=self.name, ids=item.id, action="create")
        return item

    def update(self, id, **kwargs):
        old_item = self.session.query(self.table).filter_by(id=id).first()
        old_item = copy.deepcopy(old_item)
        self.before_update(old_item)
        self.check_input(old_item, **kwargs)

        updated_fields = []
        for k, v in kwargs.items():
            if getattr(old_item, k) != v and k not in self.excluded_fields_for_log:
                updated_fields.append("%s: %s->%s" % (k, getattr(old_item, k), v))

        self.session.query(self.table).filter_by(id=id).update(kwargs)
        self.session.commit()

        new_item = self.session.query(self.table).filter_by(id=id).first()
        self.after_update(old_item, new_item)

        if self.enable_log:
            self.app.gmlog(model=self.name, ids=old_item.id, action="update", details=", ".join(updated_fields))

        return new_item

    def soft_delete_action(self, item):
        pass

    def before_delete(self, item):
        pass

    def before_soft_delete(self, item):
        pass

    def before_create(self, item):
        pass

    def check_input(self, old_item, **kwargs):
        pass

    def before_update(self, item):
        pass

    def after_create(self, item):
        pass

    def after_update(self, old_item, new_item):
        pass
