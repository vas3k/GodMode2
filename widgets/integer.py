from wtforms.fields.html5 import IntegerField

from godmode.widgets.base import BaseWidget


class IntegerWidget(BaseWidget):
    field = IntegerField()
    field_kwargs = {"style": "max-width: 100px;"}
