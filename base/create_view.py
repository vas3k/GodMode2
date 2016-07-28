from flask import request, render_template

from base.view import BaseView
from common.acl import ACL
from common.exceptions import Rejected


class BaseCreateView(BaseView):
    title = "Create"
    name = "create"
    template = "create.html"
    acl = ACL.ADMIN

    def get(self):
        return self.render(form=self.form())

    def post(self):
        form = self.form(request.form)

        if not form.validate():
            return render_template("error.html", message="Validation errors:", form_errors=form.errors)

        values = {}
        for field in form:
            field_obj = getattr(form, field.name, None)
            if field_obj is not None:
                data = field_obj.data
                if data is None or data is "":
                    # data is empty, so if field is nullable it's considered as null
                    widget = self.all_widgets.get(field.name)
                    if widget and widget.nullable:
                        data = None
                values[field.name] = data

        try:
            self.model.create(**values)
        except Exception as ex:
            raise Rejected("Save error: {}".format(ex))

        return render_template("success.html", message="Successfully created.")
