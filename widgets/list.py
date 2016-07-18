from base.widget import BaseWidget


class ListWidget(BaseWidget):
    items = []

    def render_list(self, item):
        value = getattr(item, self.name, None)
        for k, v in self.items:
            if k == value:
                return str(v)
        return str(value)

    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        template = "<select name='%s'>" % self.name
        for k, v in self.items:
            if k == value:
                template += "<option value='%s' selected='selected'>%s</option>" % (k, v)
            else:
                template += "<option value='%s'>%s</option>" % (k, v)
        template += "</select>"
        return template
