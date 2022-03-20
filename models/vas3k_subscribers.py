from database.vas3kru import Subscriber, vas3k_database
from godmode.models import BaseAdminModel
from godmode.views.list_view import BaseListView
from groups.main import Vas3kGroup


class SubscriberAdminModel(BaseAdminModel):
    db = vas3k_database
    table = Subscriber
    name = "subscribers"
    title = "Подписчики"
    icon = "icon-adduseralt"
    group = Vas3kGroup
    index = 800
    ordering = Subscriber.created_at.desc()
    details_view = None
