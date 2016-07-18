from flask import render_template, request

from base.view import BaseView
from common.acl import ACL
from common.exceptions import BadParams, Rejected


class BaseEditView(BaseView):
    title = "Edit"
    name = "edit"
    template = "edit.html"
    acl = ACL.ADMIN

    def get(self, id):
        item = self.model.get(id=id)
        if not item:
            return render_template("error.html", message="Looks like this %s item does not exist." % self.model.name)
        return self.render(item=item)

    def post(self, id):
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
                values[column_name] = widget.parse_value(value)
            except Exception as ex:
                raise BadParams("Error in field '%s' ('%s'): %s" % (column_name, value, ex))

        if "id" not in values:
            values["id"] = id

        try:
            item = self.model.update(**values)
        except Exception as ex:
            raise Rejected("Save error: %s" % ex)

        return render_template("success.html", message="Successfully saved")
