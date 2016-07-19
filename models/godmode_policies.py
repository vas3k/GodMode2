from flask import g

from base.create_view import BaseCreateView
from base.delete_view import BaseDeleteView
from base.edit_view import BaseEditView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from base.widget import BaseWidget
from common.acl import ACL
from groups.godmode import GodModeGroup
from db.godmode import PoliciesTable, UsersTable, GodModeDatabase
from widgets.boolean import BooleanWidget


class PolicyUserWidget(BaseWidget):
    def render_list(self, item):
        session = g.db_session[GodModeDatabase.__name__]
        user = session.query(UsersTable).filter_by(id=item.godmode_user_id).first()
        if user:
            return "{} ({})".format(item.godmode_user_id, user.login)
        else:
            return "<b>No such user ({})</b>".format(item.godmode_user_id)


class GodModePoliciesAdminModel(BaseAdminModel):
    acl = ACL.ADMIN
    db = GodModeDatabase
    table = PoliciesTable
    name = "gomode_policies"
    title = "Policies"
    group = GodModeGroup
    index = 60
    icon = "icon-unlock"

    fields = [
        "id",
        ("godmode_user_id", {"widget": PolicyUserWidget}),
        "policy",
        "params",
        ("has_access", {"widget": BooleanWidget}),
        ("is_enabled", {"widget": BooleanWidget})
    ]

    class PolicyListView(BaseListView):
        acl = ACL.ADMIN
        sorting = [
            "id",
            "godmode_user_id",
            "policy"
        ]

    list_view = PolicyListView

    class PolicyCreateView(BaseCreateView):
        acl = ACL.SUPERUSER

    create_view = PolicyCreateView

    class PolicyEditView(BaseEditView):
        acl = ACL.SUPERUSER

    edit_view = PolicyEditView

    class PolicyDeleteView(BaseDeleteView):
        acl = ACL.SUPERUSER

    delete_view = PolicyDeleteView

    details_view = None
