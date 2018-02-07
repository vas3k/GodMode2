from db.vas3kru import Vas3kDatabase, ClickersEN
from groups.main import Vas3kGroup
from models.vas3k_clickers import ClickersAdminModel


class ClickersENAdminModel(ClickersAdminModel):
    db = Vas3kDatabase
    table = ClickersEN
    name = "clickers_en"
    title = "Кликеры EN"
    icon = "icon-mouse"
    group = Vas3kGroup
    index = 400
    ordering = ClickersEN.created_at.desc()
