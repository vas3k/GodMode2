from flask import render_template

from base.widget import BaseWidget


class IntegerWidget(BaseWidget):
    def render_edit(self, item=None):
        value = self.render_list(item)
        return render_template("widgets/edit/number.html", name=self.name, value=value, default=self.default)

    def parse_value(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except ValueError:
            return value
