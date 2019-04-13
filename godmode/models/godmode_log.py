from godmode.views.delete_view import BaseDeleteView
from godmode.views.edit_view import BaseEditView
from godmode.views.list_view import BaseListView
from godmode.models.base import BaseAdminModel
from godmode.widgets.base import BaseWidget
from godmode.acl import ACL
from godmode.groups.godmode import GodModeGroup
from godmode.database.godmode import LogTable, GodModeDatabase


class IdsWidget(BaseWidget):
    def render_list(self, item):
        return "<a href='/models/{}/?filter=id={}'>{}</a>".format(item.model, item.ids, item.ids)


class GodModeLogAdminModel(BaseAdminModel):
    acl = ACL.ADMIN
    db = GodModeDatabase
    table = LogTable
    name = "godmode_log"
    title = "Audit log"
    icon = "icon-rawaccesslogs"
    group = GodModeGroup
    index = 20
    enable_log = False

    class LogListView(BaseListView):
        actions = []
        acl = ACL.ADMIN

    list_view = LogListView

    class LogEditView(BaseEditView):
        acl = ACL.ADMIN
        display = ["reason"]

    edit_view = LogEditView

    class LogDeleteView(BaseDeleteView):
        acl = ACL.SUPERUSER

    delete_view = LogDeleteView

    create_view = None
    details_view = None
