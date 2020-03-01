from database.vas3kru import CommentEN, vas3k_database
from groups.main import Vas3kGroup
from models.vas3k_comments import CommentAdminModel


class CommentENAdminModel(CommentAdminModel):
    db = vas3k_database
    table = CommentEN
    name = "comments_en"
    title = "Комментарии EN"
    icon = "icon-post"
    group = Vas3kGroup
    index = 800
    ordering = CommentEN.created_at.desc()
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
