from flask import render_template

from base.widget import BaseWidget


class PasswordWidget(BaseWidget):
    template = "widgets/text.html"

    def render_list(self, item):
        return "[password]"

    def render_edit(self, item=None):
        return render_template(self.template, name=self.name, value="", default=self.default)
