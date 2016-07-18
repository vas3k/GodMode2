import random
from collections import defaultdict
from datetime import datetime, timedelta

from base.model import BaseAdminModel
from base.view import BaseView
from common.acl import ACL
from tables.demo import DemoDatabase


class RetentionAdminModel(BaseAdminModel):
    db = DemoDatabase
    name = "retention"
    title = "Retention"
    place = "navbar"

    class RetentionView(BaseView):
        url = "/"
        title = "Retention stats"
        template = "plugins/retention.html"
        acl = ACL.ADMIN

        def get(self):
            totals = defaultdict(lambda: 1)
            for i in range(14):
                totals[(datetime.utcnow() - timedelta(days=i)).date()] = random.randint(10, 100)

            column_dates = list(range(0, 15))
            row_dates = [datetime.now().date() - timedelta(days=i) for i in range(0, 15)]
            table = [[random.random() for i in range(15)] for j in range(15)]

            return self.render(**{
                "data": {
                    "title": "all",
                    "row_dates": row_dates,
                    "totals": totals,
                    "column_dates": column_dates,
                    "retention": table
                }
            })

    list_view = RetentionView
