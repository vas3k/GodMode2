import jinja2

from widgets.text import TextWidget


class LongTextWidget(TextWidget):
    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        value = str(value if value is not None else "")
        value = jinja2.escape(value)
        return """<textarea name='%s'>%s</textarea>""" % (self.name, value)
