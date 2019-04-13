from database.vas3kru import Vas3kDatabase, Clickers
from godmode.models import BaseAdminModel
from groups.main import Vas3kGroup


class ClickersAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Clickers
    name = "clickers"
    title = "Кликеры"
    icon = "icon-mouse"
    group = Vas3kGroup
    index = 400
    ordering = Clickers.created_at.desc()
