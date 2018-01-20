import os
from flask import Flask, request, Response
from config import config, Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

basedir = os.path.abspath(os.path.dirname(__file__))


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.user_login'


def create_blog():
    blog = Flask(__name__)
    blog.config.from_object(Config)
    Config.init_blog(blog)

    bootstrap.init_app(blog)
    db.init_app(blog)
    login_manager.init_app(blog)

    from .main import main as main_buleprint
    blog.register_blueprint(main_buleprint)

    from .auth import auth as auth_buleprint
    blog.register_blueprint(auth_buleprint, url_prefix='/auth')

    from .manage import manage as manage_buleprint
    blog.register_blueprint(manage_buleprint, url_prefix='/manage')

    from .api_1_0 import api as api_1_0_blueprint
    blog.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return blog
