from actions.demo_ban_user import DemoBanUserAction
from godmode.views.list_view import BaseListView
from godmode.models.base import BaseAdminModel
from godmode.widgets.base import BaseWidget
from groups.demo_group import DemoGroup
from database.demo import User, DemoDatabase
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
    widgets = {
        "is_locked": BooleanReverseWidget
    }

    class PUsersListView(BaseListView):
        title = "User list"
        sorting = ["id", "name"]
        default_sorting = User.created_at.desc()
        fields = [
            "id",
            "name",
            "created_at",
            "post_count",
            "is_locked"
        ]
        object_actions = [DemoBanUserAction]
        batch_actions = [DemoBanUserAction]
        widgets = {
            "name": NameWidget
        }

    list_view = PUsersListView
