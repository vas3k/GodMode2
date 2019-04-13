from flask import Flask


def teardown_appcontext_middleware(app: Flask):
    app.teardown_appcontext_funcs = [
        # add middleware functions here
    ]
