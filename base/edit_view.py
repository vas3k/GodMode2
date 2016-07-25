from flask import render_template, request

from base.view import BaseView
from common.acl import ACL
from common.exceptions import Rejected


class BaseEditView(BaseView):
    title = "Edit"
    name = "edit"
    template = "edit.html"
    acl = ACL.ADMIN

    def get(self, id):
        item = self.model.get(id=id)
        if not item:
            return render_template("error.html", message="Looks like this {} does not exist.".format(self.model.name))
        return self.render(item=item, form=self.form(obj=item))

    def post(self, id):
        form = self.form(request.form)

        if not form.validate():
            return render_template("error.html", message="Validation errors:", form_errors=form.errors)

        updates = {}
        for field in form:
            field_obj = getattr(form, field.name, None)
            if field_obj is not None:
                updates[field.name] = field_obj.data

        if "id" not in updates:
            updates["id"] = id

        try:
            self.model.update(**updates)
        except Exception as ex:
            raise Rejected("Save error: {}".format(ex))

        return render_template("success.html", message="Successfully saved.")

