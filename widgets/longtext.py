from widgets.text import TextWidget


class LongTextWidget(TextWidget):
    def render_edit(self, item=None):
        value = self.render_list(item)
        return """<textarea name="{}">{}</textarea>""".format(self.name, value)
