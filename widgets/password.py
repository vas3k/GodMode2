import wtforms

from base.widget import BaseWidget


class PasswordWidget(BaseWidget):
    field = wtforms.PasswordField()

    def render_list(self, item):
        return "[password]"
