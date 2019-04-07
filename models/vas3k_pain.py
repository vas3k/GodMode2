from base.list_view import BaseListView
from base.model import BaseAdminModel
from db.vas3kru import Pain, Vas3kDatabase
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class PainAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Pain
    name = "pain"
    title = "Расскажи где болит"
    icon = "icon-trolleyfull"
    group = Vas3kGroup
    index = 700
    ordering = Pain.created_at.desc()
    widgets = {
        "problem": LongTextWidget,
        "solution": LongTextWidget
    }

    class PainListView(BaseListView):
        fields = [
            "id", "author", "problem", "created_at", "approved_at", "is_visible", "ip", "rating"
        ]

    list_view = PainListView

    details_view = None
