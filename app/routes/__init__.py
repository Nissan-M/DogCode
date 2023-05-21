from flask import Flask
from .home import home
from .login import login
from .auth import auth
from .courses import courses
from .teachers import teachers
from .admin import admin


def register_routes(app: Flask):
    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(login)
    app.register_blueprint(courses)
    app.register_blueprint(teachers)
    app.register_blueprint(admin)
