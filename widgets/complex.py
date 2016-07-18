from base.widget import BaseWidget


class ComplexWidget(BaseWidget):
    def render_list(self, row):
        return "[BINARY]"
