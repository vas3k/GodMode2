from db.vas3kru import CommentEN, Vas3kDatabase
from groups.main import Vas3kGroup
from models.vas3k_comments import CommentAdminModel


class CommentENAdminModel(CommentAdminModel):
    db = Vas3kDatabase
    table = CommentEN
    name = "comments_en"
    title = "Комментарии EN"
    icon = "icon-post"
    group = Vas3kGroup
    index = 800
    ordering = CommentEN.created_at.desc()
