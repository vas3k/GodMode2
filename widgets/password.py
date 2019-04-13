import wtforms

from godmode.widgets.base import BaseWidget


class PasswordWidget(BaseWidget):
    field = wtforms.PasswordField()

    def render_list(self, item):
        return "[password]"
