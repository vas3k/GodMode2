from base.delete_view import BaseDeleteView
from base.edit_view import BaseEditView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from base.widget import BaseWidget
from common.acl import ACL
from groups.godmode import GodModeGroup
from db.godmode import LogTable, GodModeDatabase


class IdsWidget(BaseWidget):
    def render_list(self, item):
        return "<a href='/models/{}/?filter=id={}'>{}</a>".format(item.model, item.ids, item.ids)


class GodModeLogAdminModel(BaseAdminModel):
    acl = ACL.ADMIN
    db = GodModeDatabase
    table = LogTable
    name = "godmode_log"
    title = "Admin log"
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
