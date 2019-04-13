from godmode.views.create_view import BaseCreateView
from godmode.views.delete_view import BaseDeleteView
from godmode.views.list_view import BaseListView
from godmode.models.base import BaseAdminModel
from godmode.acl import ACL
from godmode.groups.godmode import GodModeGroup
from godmode.database.godmode import SessionsTable, GodModeDatabase


class GodModeSessionsAdminModel(BaseAdminModel):
    acl = ACL.SUPERUSER
    db = GodModeDatabase
    table = SessionsTable
    name = "godmode_sessions"
    title = "User sessions"
    group = GodModeGroup
    index = 50
    icon = "icon-authentication-keyalt"

    fields = [
        "id",
        "user_id",
        "token",
        "created_at",
        "updated_at"
    ]

    class SessionListView(BaseListView):
        acl = ACL.SUPERUSER

    list_view = SessionListView

    class SessionDeleteView(BaseDeleteView):
        acl = ACL.SUPERUSER

    delete_view = SessionDeleteView

    class SessionEditView(BaseDeleteView):
        acl = ACL.SUPERUSER

    edit_view = SessionEditView

    class SessionCreateView(BaseCreateView):
        acl = ACL.SUPERUSER

    create_view = SessionCreateView
    details_view = None
