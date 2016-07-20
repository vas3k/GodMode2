from base.widget import BaseWidget


class PasswordWidget(BaseWidget):
    def render_list(self, item):
        return "[password]"

    def render_edit(self, item=None):
        return "<input type='text' name='{}' value='{}'>".format(self.name)
