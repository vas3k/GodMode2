from base.list_view import BaseListView
from base.model import BaseAdminModel
from base.widget import BaseWidget
from db.vas3kru import Comment, Vas3kDatabase
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class AvatarWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        return """<div style="display: inline-block; width: 40px; height: 40px; background-repeat: no-repeat; background-size: cover; border-radius: 50%%; background-image: url('http://vas3k.ru/static/images/avatars/%s');"></div>""" % item.avatar


class CommentAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Comment
    name = "comments"
    title = "Комментарии"
    icon = "icon-post"
    group = Vas3kGroup
    index = 800
    ordering = Comment.created_at.desc()
    widgets = {
        "avatar": AvatarWidget,
        "text": LongTextWidget
    }

    class CommentListView(BaseListView):
        fields = [
            "id", "avatar", "author", "text", "ip", "rating", "is_visible"
        ]

    list_view = CommentListView

    details_view = None
