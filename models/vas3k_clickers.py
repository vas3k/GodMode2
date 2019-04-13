from database.vas3kru import vas3k_database, Clickers
from godmode.models import BaseAdminModel
from groups.main import Vas3kGroup


class ClickersAdminModel(BaseAdminModel):
    db = vas3k_database
    table = Clickers
    name = "clickers"
    title = "Кликеры"
    icon = "icon-mouse"
    group = Vas3kGroup
    index = 400
    ordering = Clickers.created_at.desc()
