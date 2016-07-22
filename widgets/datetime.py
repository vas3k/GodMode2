from datetime import datetime, date

from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Optional

from base.widget import BaseWidget


class DatetimeWidget(BaseWidget):
    field = DateTimeLocalField(format="%Y-%m-%dT%H:%M:%S", validators=[Optional()])
    field_kwargs = {"step": 1}

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
