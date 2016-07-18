from common.acl import ACL


class BaseGroup(object):
    acl = ACL.ADMIN
    name = None
    policy = None
    index = None
