import wtforms
from wtforms.validators import Optional

from godmode.widgets.base import BaseWidget


class FloatWidget(BaseWidget):
    field = wtforms.FloatField(validators=[Optional()])

    def render_list(self, item):
        value = getattr(item, self.name, None)
        try:
            return round(value, 3)
        except ValueError:
            return value
