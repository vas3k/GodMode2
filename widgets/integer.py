from wtforms.fields.html5 import IntegerField

from base.widget import BaseWidget


class IntegerWidget(BaseWidget):
    field = IntegerField()
    field_kwargs = {"style": "max-width: 100px;"}
