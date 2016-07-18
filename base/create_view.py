from flask import request, render_template

from base.view import BaseView
from common.acl import ACL
from common.exceptions import BadParams, Rejected


class BaseCreateView(BaseView):
    title = "Create"
    name = "create"
    template = "create.html"
    acl = ACL.ADMIN

    def get(self):
        return self.render()

    def post(self):
        values = {}
        for column_name, column_options in self.fields_obj:
            if column_name not in self.display:
                continue

            value = request.form.get(column_name)
            try:
                widget = self.widgets[column_name]
            except KeyError:
                raise BadParams("Column %s is not defined in widgets" % column_name)

            try:
                parsed_value = widget.parse_value(value)
            except Exception as ex:
                raise BadParams("Error in field '%s': %s" % (widget.name, ex))

            if parsed_value is not None:
                values[widget.name] = parsed_value

        try:
            item = self.model.create(**values)
        except Exception as ex:
            raise Rejected("Save error: %s" % ex)

        return render_template("success.html", message="Successfully created")
