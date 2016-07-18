import logging

import settings
from base.view import BaseView
from common.acl import ACL

log = logging.getLogger(settings.APP_CODE)


class BaseDetailsView(BaseView):
    title = "Details"
    name = "details"
    layout = "table"
    template = "details.html"
    fields = None
    display = None
    actions = []
    acl = ACL.ADMIN

    def get(self, id):
        item = self.model.get(id=id)
        return self.render(item=item)
