from base.widget import BaseWidget


class FloatWidget(BaseWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        try:
            return round(value, 3)
        except:
            return value

    def parse_value(self, value):
        if value is None or value == "":
            return None

        try:
            return float(value)
        except ValueError:
            return value
