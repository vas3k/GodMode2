from datetime import datetime, date

from wtforms.fields.html5 import DateTimeField

from godmode.widgets.base import BaseWidget


class DatetimeWidget(BaseWidget):
    field = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    field_kwargs = {"step": 1}

    def render_list(self, item):
        value = getattr(item, self.name, None)
        try:
            if isinstance(value, (date, datetime)):
                return value.strftime("%d.%m.%Y %H:%M")
            elif isinstance(value, str):
                if value.isnumeric():
                    value = datetime.utcfromtimestamp(int(value)).strftime("%d.%m.%Y %H:%M")
                else:
                    return value
            else:
                return value
        except:
            return value
