"""
Main Flask Application Initialization
"""
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect


from application.database import db,User
import config
from application.bp.homepage import homepage
from application.bp.authentication import authentication


migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
bootstrap = Bootstrap5()

def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'authentication.login'

    from application.bp.authentication import authentication
    app.register_blueprint(authentication)

    # Optional: homepage blueprint if needed by test_user_logout
    from application.bp.homepage import homepage
    app.register_blueprint(homepage)
    bootstrap.init_app(app)
    return app

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)