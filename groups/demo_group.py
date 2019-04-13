from godmode.groups.base import BaseGroup
from godmode.acl import ACL


class DemoGroup(BaseGroup):
    acl = ACL.MODERATOR
    name = "Demo"
    policy = "demo_group"
    index = 1000
