from database.vas3kru import Pain, Vas3kDatabase
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
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
        "solutions": LongTextWidget
    }

    class PainListView(BaseListView):
        fields = [
            "id", "author", "problem", "created_at", "approved_at", "is_visible", "ip", "rating"
        ]

    list_view = PainListView

    details_view = None
