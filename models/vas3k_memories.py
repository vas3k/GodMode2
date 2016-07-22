from base.list_view import BaseListView
from base.model import BaseAdminModel
from db.vas3kru import Memory, Vas3kDatabase
from groups.main import Vas3kGroup
from models.vas3k_stories import ImageWidget
from widgets.longtext import LongTextWidget


class MemoryAdminModel(BaseAdminModel):
    db = Vas3kDatabase
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
