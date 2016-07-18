from base.widget import BaseWidget


class PasswordWidget(BaseWidget):
    def render_list(self, item):
        return "[hash]"

    def render_edit(self, item=None):
        # value = getattr(item, self.name, None) if item else None
        # hide password
        value = ""
        return "<input type='text' name='%s' value='%s'>" % (self.name, value if value else "")
