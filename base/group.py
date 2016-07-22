from common.acl import ACL


class BaseGroup:
    acl = ACL.ADMIN
    name = None
    policy = None
    index = None
