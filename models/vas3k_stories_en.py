from database.vas3kru import StoryEN, vas3k_database
from godmode.models import BaseAdminModel
from godmode.views.edit_view import BaseEditView
from godmode.views.list_view import BaseListView
from godmode.widgets.base import BaseWidget
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class TitleWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        template = """<a href='http://vas3k.com/{item.type}/{item.slug}/?preview=true' target='_blank' style='color: #000; font-size: 18px; font-weight: 500;'>{item.title}</a><br><span>{item.subtitle}</span>""".format(item=item)
        return template


class ImageWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        if item.image:
            if item.image.startswith("/"):
                image = "http://vas3k.com{}".format(item.image)
            else:
                image = item.image
            template = "<img src='{}' style='width: 300px;'>".format(image)
        else:
            template = ""
        return template


class StoryENAdminModel(BaseAdminModel):
    db = vas3k_database
    table = StoryEN
    name = "stories_en"
    title = "Стори EN"
    icon = "icon-store"
    group = Vas3kGroup
    index = 1000
    ordering = StoryEN.created_at.desc()
    widgets = {
        "image": ImageWidget,
        "title": TitleWidget,
        "text": LongTextWidget,
        "html": LongTextWidget
    }

    class StoryListView(BaseListView):
        fields = [
            "id", "title", "image", "type", "created_at",
            "comments_count", "views_count", "is_visible", "is_commentable"
        ]

    list_view = StoryListView

    class StoryEditView(BaseEditView):
        fields = [
            "type", "slug", "author", "title", "subtitle",
            "image", "text",
            "preview_image", "preview_text",
            "book_image", "book_text",
            "data", "created_at", "comments_count", "views_count",
            "is_visible", "is_commentable", "is_featured"
        ]

    edit_view = StoryEditView

    details_view = None

    def after_update(self, old_item, new_item):
        if old_item.text != new_item.text:
            self.session.execute(
                "update stories set text_cache = '', text_cache_rss = '' where id = :story_id",
                {"story_id": new_item.id}
            )
            self.session.commit()
