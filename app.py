import settings
from godmode import GodModeApp
from tables.demo import DemoDatabase

app = GodModeApp(databases=[DemoDatabase])
if settings.DEBUG:
    app.run()
