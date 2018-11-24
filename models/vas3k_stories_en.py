from db.vas3kru import Vas3kDatabase, StoryEN
from groups.main import Vas3kGroup
from models.vas3k_stories import StoryAdminModel


class StoryENAdminModel(StoryAdminModel):
    db = Vas3kDatabase
    table = StoryEN
    name = "stories_en"
    title = "Стори EN"
    icon = "icon-store"
    group = Vas3kGroup
    index = 1000
    ordering = StoryEN.created_at.desc()

    class StoryListView(BaseListView):
        fields = [
            "id", "title", "image", "type", "created_at",
            "comments_count", "views_count", "is_visible", "is_commentable"
        ]

    list_view = StoryListView

    class StoryEditView(BaseEditView):
        fields = [
            "type", "slug", "author", "title", "subtitle",
            "image", "text", "html", "preview_image", "preview_text",
            "data", "created_at", "comments_count", "views_count",
            "is_visible", "is_commentable", "is_featured"
        ]

    edit_view = StoryEditView

    details_view = None

    def after_update(self, old_item, new_item):
        if old_item.text != new_item.text:
            self.session.execute(
                "update stories_en set text_cache = '', text_cache_rss = '' where id = :story_id",
                {"story_id": new_item.id}
            )
            self.session.commit()
