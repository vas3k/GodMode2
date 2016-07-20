import json

import jinja2
from flask import render_template

from base.widget import BaseWidget


class ArrayWidget(BaseWidget):
    filterable = False

    @property
    def default(self):
        return "[]"

    def render_edit(self, item=None):
        value = getattr(item, self.name, None)
        if value:
            if isinstance(value, str):
                value = json.loads(value)
            value = jinja2.escape(json.dumps(value))
        return render_template("widgets/edit/text.html", name=self.name, value=value, default=self.default)

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
