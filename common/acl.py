from flask import g

from tables.godmode import PoliciesTable, GodModeDatabase


class ACL(object):
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

        has_access = False

        if module.acl == ACL.OPEN:
            return True

        if user is None:
            return False

        policy_list = []
        if module.policy:
            session = g.db_session[GodModeDatabase.__name__]
            module_policy_list = module.policy.split('.')
            policy_string = ""
            for module_policy in module_policy_list:
                policy_string = "{}.{}".format(policy_string, module_policy).strip('.')
                policy = session.query(PoliciesTable).filter_by(
                        godmode_user_id=user.id,
                        policy=policy_string,
                        is_enabled=1
                )
                policy = policy.filter(PoliciesTable.params.is_(None)).first()
                if policy:
                    policy_list.append(policy)

        if policy_list:
            for policy in policy_list:
                has_access = policy.has_access
            return has_access

        # try:
        if cls.PRIORITY.index(user.acl) <= cls.PRIORITY.index(module.acl):
            has_access = True
        else:
            has_access = False
        # except (ValueError, KeyError):
        #     raise AccessDenied("Not valid user ACL: '%s', or module ACL: '%s'" % (user.acl, module_acl))
        return has_access

    @classmethod
    def filter_items(cls, user, module):
        if user is None or module is None:
            return None

        try:
            module_items = module.items[:]
            is_list = True
        except TypeError:
            module_items = [module.items]
            is_list = False

        if not module_items:
            return module.items

        session = g.db_session[GodModeDatabase.__name__]
        module_policy = session.query(PoliciesTable).filter_by(
                godmode_user_id=user.id,
                policy=module.policy,
                is_enabled=1
        )
        policy = module_policy.filter(PoliciesTable.params.isnot(None)).first()

        if not policy:
            return module.items

        new_items = []
        params_string = policy.params
        param_list = []
        params_list = params_string.split(",")

        for param in params_list:
            is_integer = True
            param_split = param.split(".")
            try:
                param_attribute = param_split[0].strip(' ')
                param_value = param_split[1].strip(' ')
            except IndexError:
                continue

            try:
                int(param_value.replace("-", ""))
            except ValueError:
                is_integer = False

            if "-" in param_value and is_integer:
                range_item = param_value.split("-")
                try:
                    range_start = int(range_item[0])
                    range_stop = int(range_item[1])
                except ValueError:
                    continue

                if range_start < range_stop:
                    param_list.append({
                        "attribute": param_attribute,
                        "value": (range_start, range_stop),
                        "range": True
                    })
                elif range_start > range_stop:
                    param_list.append({
                        "attribute": param_attribute,
                        "value": (range_stop, range_start),
                        "range": True
                    })
                else:
                    param_list.append({
                        "attribute": param_attribute,
                        "value": range_start,
                        "range": False
                    })
            else:
                try:
                    param_list.append({
                        "attribute": param_attribute,
                        "value": int(param_value),
                        "range": False
                    })
                except ValueError:
                    none_values = [
                        "None",
                        "none",
                        "Null",
                        "null"
                    ]
                    true_values = ["True", "true"]
                    false_values = ["False", "false"]

                    if param_value in none_values:
                        param_value = None
                    elif param_value in false_values:
                        param_value = 0
                    elif param_value in true_values:
                        param_value = 1
                    param_list.append({
                        "attribute": param_attribute,
                        "value": param_value,
                        "range": False
                    })
            try:
                if param_list:
                    getattr(module_items[0], param_list[-1].get("attribute"))
            except AttributeError:
                param_list.pop()

        if not param_list:
            return module.items

        # Это можно как-то быстрее сделать? 1000 items x 50 params = 50k iterations.
        if not policy.has_access:
            new_items = module_items[:]

        for item in module_items:
            for param in param_list:
                try:
                    item_value = int(getattr(item, param.get("attribute")))
                except (ValueError, TypeError):
                    item_value = getattr(item, param.get("attribute"))
                param_value = param.get("value")
                if not param.get("range"):
                    if policy.has_access:
                        if (item_value == param_value or item_value is param_value) and item not in new_items:
                            new_items.append(item)
                            break
                    else:
                        if (item_value == param_value or item_value is param_value) and item in new_items:
                            new_items.remove(item)
                            break
                else:
                    range_start = param_value[0]
                    range_stop = param_value[1]

                    if policy.has_access:
                        if range_start <= item_value <= range_stop and item not in new_items:
                            new_items.append(item)
                            break
                    else:
                        if range_start <= item_value <= range_stop and item in new_items:
                            new_items.remove(item)
                            break
        if not is_list and new_items:
            return new_items[0]
        return new_items
