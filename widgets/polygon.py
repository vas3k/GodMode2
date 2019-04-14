import wtforms
from flask import render_template

from godmode.widgets.base import BaseWidget


class PolygonWidget(BaseWidget):
    filterable = False
    field = wtforms.TextAreaField()

    def render_list(self, item):
        value = getattr(item, self.name, None) if item else None
        value = str(value if value is not None else "")
        maps_path = value[2:-2].replace("),(", "|")
        return "<img src='http://maps.googleapis.com/maps/api/staticmap?size=300x100" \
               "&path=color:0xff0000|fillcolor:0xAA000033|weight:1|%s" \
               "&sensor=false&key=AIzaSyAicgdCqN5zzZJMLSMdlgUf17tPY0eyrr8'>" % maps_path

    def render_edit(self, form=None, item=None):
        value = getattr(item, self.name, None) if item else None
        value = str(value if value is not None else "")
        value = value.replace('"', "&quot;")
        return render_template("widgets/polygon.html", name=self.name, value=value, form=form)
