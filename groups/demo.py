from base.group import BaseGroup
from common.acl import ACL


class DemoGroup(BaseGroup):
    acl = ACL.MODERATOR
    name = "Demo"
    policy = "demo_group"
    index = 1000
