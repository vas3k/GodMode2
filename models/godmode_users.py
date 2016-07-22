import bcrypt
from flask import g

from base.create_view import BaseCreateView
from base.delete_view import BaseDeleteView
from base.edit_view import BaseEditView
from base.list_view import BaseListView
from base.model import BaseAdminModel
from common.acl import ACL
from common.api import API
from common.exceptions import ObjectNotFound, AccessDenied, AuthFailed
from groups.godmode import GodModeGroup
from db.godmode import LogTable
from db.godmode import SessionsTable, UsersTable, GodModeDatabase
from widgets.list import ListWidget
from widgets.password import PasswordWidget


class AclWidget(ListWidget):
    items = [(acl, acl) for acl in ACL.PRIORITY]


class GodModeUsersAdminModel(BaseAdminModel):
    acl = ACL.ADMIN
    db = GodModeDatabase
    table = UsersTable
    name = "godmode_users"
    title = "Admin users"
    icon = "icon-useralt"
    group = GodModeGroup
    index = 100
    excluded_fields_for_log = ["password"]

    fields = [
        "id",
        "login",
        "acl",
        "password",
        "created_at",
        "updated_at"
    ]

    widgets = {
        "acl": AclWidget,
        "password": PasswordWidget
    }

    class UserListView(BaseListView):
        acl = ACL.ADMIN
        title = "User list"
        sorting = ["id", "acl", "created_at"]
        display = [
            "id",
            "login",
            "acl",
            "created_at",
            "updated_at"
        ]

    list_view = UserListView

    class UserEditView(BaseEditView):
        acl = ACL.SUPERUSER

    edit_view = UserEditView

    class UserDeleteView(BaseDeleteView):
        acl = ACL.SUPERUSER

    delete_view = UserDeleteView

    class UserCreateView(BaseCreateView):
        acl = ACL.SUPERUSER

    create_view = UserCreateView

    details_view = None

    def before_create(self, item):
        item.password = self.hash_password(item.password)

    def after_update(self, old_item, new_item):
        new_password = new_item.password
        if new_password:
            new_password_hash = self.hash_password(new_password)
            self.session.query(self.table).filter_by(id=new_item.id).update(dict(password=new_password_hash))
            self.session.commit()
        else:
            self.session.query(self.table).filter_by(id=new_item.id).update(dict(password=old_item.password))
            self.session.commit()

        if old_item.login != new_item.login:
            self.session.query(LogTable).filter_by(user=old_item.login).update(dict(user=new_item.login))
            self.session.commit()

    @classmethod
    def login(cls, request, login, password):
        session = g.db_session[GodModeDatabase.__name__]
        user = session.query(UsersTable).filter_by(login=login).first()
        if not user:
            raise ObjectNotFound("Wrong username.")

        if not cls.check_password(user, password):
            raise AccessDenied("Wrong password.")

        client = SessionsTable(
                user_id=user.id,
                token=API.generate_hash(user.id)
        )
        session.add(client)
        session.commit()

        return user, client

    @classmethod
    def logout(cls, request):
        user, client = yield cls.user(request, with_client=True)
        session = g.db_session[GodModeDatabase.__name__]
        session.delete(client)
        session.flush()
        return True

    @classmethod
    def user(cls, request, with_client=False):
        user_id = API.get_int(request, "gm_user_id")
        token = API.get_str(request, "gm_token")
        session = g.db_session[GodModeDatabase.__name__]
        client = session.query(SessionsTable).filter_by(user_id=user_id, token=token).first()
        if not client:
            raise AuthFailed("Auth failed")

        user = session.query(UsersTable).filter_by(id=client.user_id).first()
        if with_client:
            return user, client
        else:
            return user

    @classmethod
    def hash_password(cls, password):
        bcypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        if isinstance(bcypted_password, bytes):
            return bcypted_password.decode("utf-8")
        return bcypted_password

    @classmethod
    def check_password(cls, user, raw_password):
        is_valid = bcrypt.checkpw(raw_password, user.password)
        return is_valid
