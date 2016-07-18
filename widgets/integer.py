from base.widget import BaseWidget


class IntegerWidget(BaseWidget):
    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        return "<input type='number' name='%s' value='%s' style='width: 100px;'>" % (self.name, value if value is not None else "")

    def parse_value(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except ValueError:
            return value
