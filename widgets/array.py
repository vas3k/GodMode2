import json

import jinja2

from base.widget import BaseWidget


class ArrayWidget(BaseWidget):
    filterable = False

    def render_edit(self, item=None):
        value = str(getattr(item, self.name, None) or "")
        if value:
            value = value.replace('"', "&quot;")
            value = value.replace("'", '"')
            value = value.replace("None", "null")  # FIXME: блядь как же это хуево, но нет времени
            value = json.loads(value)
        return """<input type="text" name="%s" value="%s">""" % (self.name, jinja2.escape(json.dumps(value) if value else "[]"))

    def parse_value(self, value):
        if not value and self.meta is not None:
            if self.meta.default:
                return self.meta.default
            elif self.meta.server_default:
                return self.meta.server_default
            elif self.meta.nullable:
                return None
        try:
            return json.loads(value) or []
        except Exception as ex:
            raise Exception("Bad param for field '{}': {} ({})".format(self.name, value, ex))
