# This file deals with things which needs to be set up once only
# eg. Instance of flask app,setup database,login feature 
# once for each instance etc.
# First file which is looked up in project is _init__.py. In this 
# file currentApp() is called.

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    db.init_app(app)
    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    from .models import User
    @loginManager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # We need to register the main and auth functionalities
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app

    
