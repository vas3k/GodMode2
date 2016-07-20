from flask import render_template

from base.widget import BaseWidget


class BooleanWidget(BaseWidget):
    template = "widgets/checkbox.html"

    def render_list(self, item):
        value = getattr(item, self.name, None)
        if value:
            return "<i class='icon-ok' style='color: #0c0;'></i>"
        else:
            return "<i class='icon-remove' style='color: #c00;'></i>"

    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        return render_template(self.template, name=self.name, checked=bool(value), default=self.default)

    def parse_value(self, value):
        return bool(value)


class BooleanReverseWidget(BooleanWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        if value:
            return "<i class='icon-ok' style='color: #c00;'></i>"
        else:
            return "<i class='icon-remove' style='color: #0c0;'></i>"
