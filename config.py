# coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!@#$%^&*12345678'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1234@localhost:3306/weblog'
    # 邮件系统配置
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    FLASKY_MAIL_SENDER = "Weblog Admin <540918220@qq.com>"
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '540918220@qq.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Weblog]'

    @staticmethod
    def init_blog(blog):
        pass


class DevelopmentConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
}
