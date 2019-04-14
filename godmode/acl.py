class ACL:
    SUPERUSER = "superuser"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ALL = "all"
    OPEN = "open"

    PRIORITY = [SUPERUSER, ADMIN, MODERATOR, ALL]

    @classmethod
    def has_access(cls, user, module):

        if module is None:
            return False

        if module.acl == ACL.OPEN:
            return True

        if user is None:
            return False

        has_access = cls.PRIORITY.index(user.acl) <= cls.PRIORITY.index(module.acl)

        return has_access

    @classmethod
    def filter_items(cls, user, module):
        if user is None or module is None:
            return None

        try:
            module_items = module.items[:]
            # is_list = True
        except TypeError:
            module_items = [module.items]
            # is_list = False

        if not module_items:
            return module.items

        return module.items
