import jinja2
import wtforms
from flask import render_template
from sqlalchemy.sql.elements import TextClause


class BaseWidget:
    filterable = True
    field = wtforms.StringField()
    field_kwargs = {}

    def __init__(self, name, meta, model):
        self.name = name
        self.meta = meta
        self.model = model

    @property
    def pretty_name(self):
        return self.name.replace("_", " ")

    @property
    def default(self):
        if self.meta.default or self.meta.server_default:
            default = (self.meta.default or self.meta.server_default).arg
            if isinstance(default, TextClause):
                default = ""
        else:
            default = ""
        return default

    def render_edit(self, form=None, item=None):
        if form:
            return form[self.name](**self.field_kwargs)
        value = str(getattr(item, self.name, None) or "")
        value = jinja2.escape(value)
        return render_template("widgets/text.html", name=self.name, value=value, default=self.default)

    def render_list(self, item):
        value = getattr(item, self.name, None)
        return jinja2.escape(str(value)) if value is not None else "null"

    def render_details(self, item):
        return self.render_list(item)
