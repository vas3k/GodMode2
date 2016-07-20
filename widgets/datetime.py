from datetime import datetime, date

from base.widget import BaseWidget


class DatetimeWidget(BaseWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        try:
            if isinstance(value, (date, datetime)):
                return value.strftime("%d.%m.%Y&nbsp;%H:%M")
            elif isinstance(value, str):
                if value.isnumeric():
                    value = datetime.utcfromtimestamp(int(value)).strftime("%d.%m.%Y&nbsp;%H:%M")
                else:
                    return value
            else:
                return value
        except:
            return value

    def render_edit(self, item=None):
        value = self.render_list(item)
        return "<input type='datetime-local' name='%s' value='%s' step='1'>" % (self.name, value or "")

    def parse_value(self, value):
        if value:
            try:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                value = datetime.strptime(value, "%Y-%m-%dT%H:%M")
        else:
            return None
        return value
