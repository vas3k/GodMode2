from flask import request, make_response, redirect

from godmode.models.base import BaseAdminModel
from godmode.views.view import BaseView
from godmode.acl import ACL
from godmode.api import API


class GodModeAuthAdminModel(BaseAdminModel):
    acl = ACL.OPEN
    url_prefix = ""
    place = None
    enable_log = False

    views = {
        "login_view": "/login/",
        "logout_view": "/logout/"
    }

    class LoginView(BaseView):
        url = "/login/"
        title = "Login"
        template = "login.html"
        acl = ACL.OPEN

        def get(self):
            context = {}
            return self.render(**context)

        def post(self):
            login = API.get_str(request, "login")
            password = API.get_str(request, "password")
            from godmode.models.godmode_users import GodModeUsersAdminModel
            user, client = GodModeUsersAdminModel.login(request, login, password)
            response = make_response(redirect("/"))
            response.set_cookie("gm_user_id", str(user.id))
            response.set_cookie("gm_token", client.token)
            return response

    login_view = LoginView

    class LogoutView(BaseView):
        url = "/logout/"
        acl = ACL.ALL

        def get(self):
            from godmode.models.godmode_users import GodModeUsersAdminModel
            GodModeUsersAdminModel.logout(request)
            response = make_response(redirect("/login/"))
            response.set_cookie("gm_user_id", "", expires=0)
            response.set_cookie("gm_token", "", expires=0)
            return response

    logout_view = LogoutView
