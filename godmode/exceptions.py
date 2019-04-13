from flask import redirect, render_template, make_response


class AlreadyInitializedException(Exception):
    pass


class GodModeException(Exception):
    status_code = 400
    template = "error.html"
    default_message = "Something went wrong"

    def __init__(self, message=None, data=None):
        Exception.__init__(self)
        self.message = message or self.default_message
        self.data = data

    def handler(self):
        response = make_response(render_template(self.template, message=self.message, data=self.data))
        response.status_code = self.status_code
        return response


class ImproperlyConfigured(GodModeException):
    default_message = "Improperly Configured"


class Rejected(GodModeException):
    default_message = "Rejected"


class AccessDenied(GodModeException):
    default_message = "Access Denied"


class AuthFailed(GodModeException):
    def handler(self):
        return redirect("/login/")


class AuthRequired(GodModeException):
    def handler(self):
        return redirect("/login/")


class BadParams(GodModeException):
    default_message = "Bad Params"


class ObjectNotFound(GodModeException):
    default_message = "Object not found"


class UnexpectedError(GodModeException):
    default_message = "Unexpected error"


class AlreadyInUse(GodModeException):
    default_message = "Already in use"


class Overlimit(GodModeException):
    default_message = "Overlimit"


class Banned(GodModeException):
    default_message = "Banned"


class AccessViolation(GodModeException):
    default_message = "Access Violation"


class Timeout(GodModeException):
    default_message = "Timeout"
