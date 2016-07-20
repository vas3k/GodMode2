from base.widget import BaseWidget


class IntegerWidget(BaseWidget):
    def render_edit(self, item=None):
        value = self.render_list(item)
        return "<input type='number' name='{}' value='{}' style='width: 100px;'>".format(self.name, value if value is not None else "")

    def parse_value(self, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except ValueError:
            return value
