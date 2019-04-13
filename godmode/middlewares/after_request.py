from flask import Flask


def after_request_middleware(app: Flask):
    app.after_request_funcs.setdefault(None, [
        # add middleware functions here
    ])
