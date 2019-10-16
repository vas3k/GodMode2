from database.vas3kru import User, vas3k_database
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
from godmode.widgets.base import BaseWidget
from groups.main import Vas3kGroup


class AvatarWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        return """<div style="display: inline-block; width: 40px; height: 40px; background-repeat: no-repeat; background-size: cover; border-radius: 50%%; background-image: url('%s');"></div>""" % item.avatar


class CommentAdminModel(BaseAdminModel):
    db = vas3k_database
    table = User
    name = "comments"
    title = "Юзеры"
    icon = "icon-user"
    group = Vas3kGroup
    index = 700
    ordering = User.created_at.desc()
    widgets = {
        "avatar": AvatarWidget
    }

    class CommentListView(BaseListView):
        fields = [
            "id", "avatar", "name", "occupation", "created_at", "membership_started_at", "is_active"
        ]

    list_view = CommentListView

    details_view = None
