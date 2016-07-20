import jinja2
from flask import render_template

from widgets.text import TextWidget


class LongTextWidget(TextWidget):
    def render_edit(self, item=None):
        value = str(getattr(item, self.name, None) or "")
        value = jinja2.escape(value)
        return render_template("widgets/edit/longtext.html", name=self.name, value=value, default=self.default)
