from database.vas3kru import vas3k_database, StoryEN
from groups.main import Vas3kGroup
from models.vas3k_stories import StoryAdminModel


class StoryENAdminModel(StoryAdminModel):
    db = vas3k_database
    table = StoryEN
    name = "stories_en"
    title = "Стори EN"
    icon = "icon-store"
    group = Vas3kGroup
    index = 1000
    ordering = StoryEN.created_at.desc()

    def after_update(self, old_item, new_item):
        if old_item.text != new_item.text:
            self.session.execute(
                "update stories_en set text_cache = '', text_cache_rss = '' where id = :story_id",
                {"story_id": new_item.id}
            )
            self.session.commit()
