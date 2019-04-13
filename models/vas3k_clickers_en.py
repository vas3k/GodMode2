from database.vas3kru import vas3k_database, ClickersEN
from groups.main import Vas3kGroup
from models.vas3k_clickers import ClickersAdminModel


class ClickersENAdminModel(ClickersAdminModel):
    db = vas3k_database
    table = ClickersEN
    name = "clickers_en"
    title = "Кликеры EN"
    icon = "icon-mouse"
    group = Vas3kGroup
    index = 400
    ordering = ClickersEN.created_at.desc()
