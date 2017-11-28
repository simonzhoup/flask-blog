from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    abortme = db.Column(db.Text())
    member_since = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    avatar = db.Column(db.String(64), default='dafulte.png')

    @property
    def password(self):
        raise AttributeError(u'密码属性不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def is_self(self, current_user):
        return current_user.is_authenticated and self.id == current_user.id

    def follow(self, followed):
        f = Follow(follower_id=self.id, followed_id=followed.id)
        db.session.add(f)

    def unfollow(self, followed):
        f = Follow.query.filter_by(
            follower_id=self.id, followed_id=followed.id).first()
        if f:
            db.session.delete(f)

    def all_follow(self):
        return Follow.query.filter_by(follower_id=self.id).all()

    def all_follower(self):
        return Follow.query.filter_by(followed_id=self.id).all()

    def is_follow(self, user):
        return Follow.query.filter_by(follower_id=self.id, followed_id=user.id).first()


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), unique=True, index=True)
    info = db.Column(db.Text())
    img = db.Column(db.String(64))
