from flask import render_template, request

from godmode.views.view import BaseView
from godmode.acl import ACL
from godmode.exceptions import Rejected


class BaseEditView(BaseView):
    title = "Edit"
    name = "edit"
    template = "edit.html"
    acl = ACL.ADMIN

    def get(self, item_id):
        item = self.model.get(id=item_id)
        if not item:
            return render_template("error.html", message="'{}' does not exist.".format(self.model.name))
        return self.render(item=item, form=self.form(obj=item))

    def post(self, item_id):
        form = self.form(request.form)

        if not form.validate():
            return render_template("error.html", message="Validation errors:", form_errors=form.errors)

        updates = {}
        for field in form:
            field_obj = getattr(form, field.name, None)
            if field_obj is not None:
                data = field_obj.data
                if data is None or data == "":  # 0 or False are ok
                    # if data is empty — nullable field considered as null
                    widget = self.all_widgets.get(field.name)
                    if widget and widget.nullable:
                        data = None
                updates[field.name] = data

        if "id" not in updates:
            updates["id"] = item_id

        try:
            self.model.update(**updates)
        except Exception as ex:
            self.model.db.session.rollback()
            raise Rejected("Error while saving: {}".format(ex))

        return render_template("success.html", message="Successfully saved.")
