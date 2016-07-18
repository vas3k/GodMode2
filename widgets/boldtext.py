from base.widget import BaseWidget


class BoldTextWidget(BaseWidget):
    def render_list(self, item):
        value = getattr(item, self.name, None)
        return "<strong style='font-size: 16px;'>%s</strong>" % value
