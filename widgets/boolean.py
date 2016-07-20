from base.widget import BaseWidget


class BooleanWidget(BaseWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        if value:
            return "<i class='icon-ok' style='color: #0c0;'></i>"
        else:
            return "<i class='icon-remove' style='color: #c00;'></i>"

    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        return "<input type='checkbox' name='{}' value='1' {}>".format(self.name, "checked='checked'" if value else "")

    def parse_value(self, value):
        return bool(value)


class BooleanReverseWidget(BooleanWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        if value:
            return "<i class='icon-ok' style='color: #c00;'></i>"
        else:
            return "<i class='icon-remove' style='color: #0c0;'></i>"
