from actions.ban import BanAction
from base.delete_view import BaseDeleteView
from base.details_view import BaseDetailsView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from base.widget import BaseWidget
from common.acl import ACL
from groups.demo import DemoGroup
from db.demo import User, DemoDatabase
from widgets.boolean import BooleanReverseWidget


class NameWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        return "<b>{}</b>".format(item.name)


class UsersAdminModel(BaseAdminModel):
    db = DemoDatabase
    name = "users"
    title = "Users"
    icon = "icon-user"
    group = DemoGroup
    index = 100
    table = User
    custom_widgets = {
        "is_locked": BooleanReverseWidget
    }

    class UsersListView(BaseListView):
        title = "User list"
        sorting = ["id", "name"]
        default_sorting = User.created_at.desc()
        fields = [
            "id",
            ("name", {"widget": NameWidget}),
            "created_at",
            "post_count",
            "is_locked"
        ]
        object_actions = [BanAction]
        batch_actions = [BanAction]

    list_view = UsersListView

    class UsersDetailsView(BaseDetailsView):
        actions = [BanAction]

    details_view = UsersDetailsView

    class UsersDeleteView(BaseDeleteView):
        acl = ACL.SUPERUSER

    delete_view = UsersDeleteView
