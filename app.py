import settings
from godmode import GodModeApp
from db.demo import DemoDatabase
from models.index import IndexAdminModel
from models.posts import PostsAdminModel
from models.retention import RetentionAdminModel
from models.users import UsersAdminModel

app = GodModeApp(
    databases=[DemoDatabase],
    models=[
        IndexAdminModel,
        PostsAdminModel,
        UsersAdminModel,
        RetentionAdminModel
    ]
)

if settings.DEBUG:
    app.run()
