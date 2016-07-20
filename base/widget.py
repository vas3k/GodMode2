import html

import jinja2


class BaseWidget:
    filterable = True

    def __init__(self, name, meta, model):
        self.name = name
        self.pretty_name = name.replace("_", " ")
        self.meta = meta
        self.model = model

    def render_list(self, item):
        value = str(getattr(item, self.name, "MISSING"))
        return jinja2.escape(value)

    def render_edit(self, item=None):
        value = str(getattr(item, self.name, None) or "")
        value = jinja2.escape(value)
        return """<input type="text" name="%s" value="%s">""" % (self.name, html.escape(value))

    def render_details(self, item):
        return self.render_list(item)

    def parse_value(self, value):
        if not value and self.meta is not None:
            if self.meta.default:
                return self.meta.default
            elif self.meta.server_default:
                return self.meta.server_default
            elif self.meta.nullable:
                return None
        return value
