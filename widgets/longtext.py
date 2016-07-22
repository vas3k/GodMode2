import wtforms

from widgets.text import TextWidget


class LongTextWidget(TextWidget):
    field = wtforms.TextAreaField()
