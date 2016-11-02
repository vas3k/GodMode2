from base.model import BaseAdminModel
from db.vas3kru import Comment, Vas3kDatabase, Clickers
from groups.main import Vas3kGroup


class ClickersAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Clickers
    name = "clickers"
    title = "Кликеры"
    icon = "icon-mouse"
    group = Vas3kGroup
    index = 400
    ordering = Comment.created_at.desc()
