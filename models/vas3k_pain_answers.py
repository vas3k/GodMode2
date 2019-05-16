from database.vas3kru import vas3k_database, PainAnswer
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class PainAnswerAdminModel(BaseAdminModel):
    db = vas3k_database
    table = PainAnswer
    name = "pain_answers"
    title = "Ответы на боли"
    icon = "icon-trolleyfull"
    group = Vas3kGroup
    index = 600
    ordering = PainAnswer.created_at.desc()
    widgets = {
        "url_description": LongTextWidget,
        "comment": LongTextWidget
    }

    class PainListView(BaseListView):
        fields = [
            "id", "pain_id", "author", "url", "url_title", "comment", "created_at", "is_visible", "ip", "rating"
        ]

    list_view = PainListView

    details_view = None
