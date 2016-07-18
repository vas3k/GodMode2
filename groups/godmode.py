from base.group import BaseGroup
from common.acl import ACL


class GodModeGroup(BaseGroup):
    acl = ACL.ADMIN
    policy = "godmode_group"
    name = "GodMode"
    index = 0
