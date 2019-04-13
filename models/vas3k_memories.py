from database.vas3kru import Memory, vas3k_database
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
from groups.main import Vas3kGroup
from models.vas3k_stories import ImageWidget
from widgets.longtext import LongTextWidget


class MemoryAdminModel(BaseAdminModel):
    db = vas3k_database
    table = Memory
    name = "memories"
    title = "Мемориз"
    icon = "icon-time"
    group = Vas3kGroup
    index = 900
    ordering = Memory.created_at.desc()
    widgets = {
        "image": ImageWidget,
        "text": LongTextWidget
    }

    class MemoryListView(BaseListView):
        fields = [
            "id", "image", "title", "subtitle", "type", "created_at", "is_visible", "story_id"
        ]

    list_view = MemoryListView
