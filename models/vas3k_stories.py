from base.edit_view import BaseEditView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from base.widget import BaseWidget
from db.vas3kru import Story, Vas3kDatabase
from groups.main import Vas3kGroup
from widgets.longtext import LongTextWidget


class TitleWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        template = """<a href='http://vas3k.ru/{item.type}/{item.slug}/?preview=true' target='_blank' style='color: #000; font-size: 18px; font-weight: 500;'>{item.title}</a><br><span>{item.subtitle}</span>""".format(item=item)
        return template


class ImageWidget(BaseWidget):
    filterable = False

    def render_list(self, item):
        if item.image:
            if item.image.startswith("/"):
                image = "http://vas3k.ru{}".format(item.image)
            else:
                image = item.image
            template = "<img src='{}' style='width: 300px;'>".format(image)
        else:
            template = ""
        return template


class StoryAdminModel(BaseAdminModel):
    db = Vas3kDatabase
    table = Story
    name = "stories"
    title = "Стори"
    icon = "icon-store"
    group = Vas3kGroup
    index = 1000
    ordering = Story.created_at.desc()
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
            "image", "text", "html", "preview_image", "preview_text",
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
