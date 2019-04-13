import json

import wtforms

from godmode.widgets.base import BaseWidget


def parse_value(value):
    try:
        return json.loads(value) if value else None
    except Exception as ex:
        raise ValueError("Bad JSON: {}".format(ex))


class JSONWidget(BaseWidget):
    filterable = False
    field = wtforms.TextAreaField(filters=[parse_value])

    def render_edit(self, form=None, item=None):
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
