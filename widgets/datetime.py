from datetime import datetime

from base.widget import BaseWidget


class DatetimeWidget(BaseWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        try:
            return value.strftime("%d.%m.%Y&nbsp;%H:%M")
        except:
            return value

    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        try:
            dt = value.strftime("%Y-%m-%dT%H:%M:%S")
        except:
            dt = None
        return "<input type='datetime-local' name='%s' value='%s' step='1'>" % (self.name, dt or "")

    def parse_value(self, value):
        if value:
            try:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M")
        else:
            return None
        return value
