import copy

import jinja2
import wtforms
from flask import render_template
from sqlalchemy.sql.elements import TextClause
from wtforms.fields.core import UnboundField
from wtforms.validators import Optional, InputRequired


class BaseWidget:
    filterable = True
    field = wtforms.StringField()
    field_kwargs = {}

    def __init__(self, name, meta, model):
        self.name = name
        self.meta = meta
        self.model = model
        self.field = copy.copy(self.field)
        if self.field is not None:
            self.field.label = self.pretty_name
            self.field.default = self.default
            if isinstance(self.field, wtforms.BooleanField) \
                    or (isinstance(self.field, UnboundField) and self.field.field_class == wtforms.BooleanField):
                # because I don't found how to handle InputRequired for BooleanField :(
                extra_validators = [Optional()]
            else:
                extra_validators = [Optional() if self.meta.nullable or self.default is not None else InputRequired()]

            self.field.kwargs["validators"] = list(set(self.field.kwargs.get("validators") or []) | set(extra_validators))

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
            default = None
        return default

    @property
    def nullable(self):
        return self.meta.nullable

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
