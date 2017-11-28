import os
from flask import Flask, request, Response
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
pymysql.install_as_MySQLdb()

basedir = os.path.abspath(os.path.dirname(__file__))


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.user_login'
q = Auth('jrFL91mRGNiP2cAuLJtOLEE5rYCzUrzw-3BMskl4',
         'S2Mj_wgFgyLi3Nkb3AqZck1lYP5XPY0phxAersbH')
bucket_name = 'flask-web'


def create_blog(config_name):
    blog = Flask(__name__)
    blog.config.from_object(config[config_name])
    config[config_name].init_blog(blog)

    bootstrap.init_app(blog)
    db.init_app(blog)
    login_manager.init_app(blog)

    # 注册蓝本
    from .main import main as main_buleprint
    blog.register_blueprint(main_buleprint)

    from .auth import auth as auth_buleprint
    blog.register_blueprint(auth_buleprint, url_prefix='/auth')

    return blog
