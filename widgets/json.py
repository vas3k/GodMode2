import json

from base.widget import BaseWidget


class JSONWidget(BaseWidget):
    filterable = False

    def render_edit(self, item=None):
        value = getattr(item, self.name, None) if item else None
        if value is not None:
            value = json.dumps(value)
        else:
            value = ""
        return """<textarea name="%s" style="height: 100px;">%s</textarea>""" % (self.name, value)

    def render_details(self, item):
        value = getattr(item, self.name, None)
        template = ""
        if value:
            for k, v in value.items():
                template += "%s: %s<br>" % (k, v)
        return template

    def parse_value(self, value):
        result = super().parse_value(value)
        if result is not None:
            return json.loads(result)
        return None
