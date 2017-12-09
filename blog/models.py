from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime
from sqlalchemy import and_, or_


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
    noread_messages = db.Column(db.Integer, index=True, default=0)
    admin = db.Column(db.Boolean(), default=False)

    @property
    def password(self):
        raise AttributeError(u'密码属性不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def admin(self):
        if User.query.count() == 1:
            self.admin = True
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

    # def read_message(self):
    #     self.noread_messages -= 1
    #     db.session.add(self)


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
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    clink = db.Column(db.Integer, default=1)
    author = db.Column(db.Integer, index=True)

    def ping(self):
        self.clink += 1
        db.session.add(self)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, index=True)
    tpoic = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    clink = db.Column(db.Integer, default=1)
    head = db.Column(db.String(64))
    body = db.Column(db.Text())

    def ping(self):
        self.clink += 1
        db.session.add(self)


class TopicFollows(db.Model):
    __tablename__ = 'topicfollows'
    user_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)

    def follow(user, topic):
        f = TopicFollows(user_id=user, topic_id=topic)
        db.session.add(f)

    def unfollow(user, topic):
        f = TopicFollows.query.filter_by(user_id=user, topic_id=topic).first()
        if f:
            db.session.delete(f)

    def is_follow(user, topic):
        return TopicFollows.query.filter_by(user_id=user, topic_id=topic).first()


class Comments(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, index=True)
    post_id = db.Column(db.Integer, index=True, nullable=True)
    post_author_id = db.Column(db.Integer, index=True)
    comment_id = db.Column(db.Integer, index=True, nullable=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    read = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime(), default=datetime.now)

    def read_comment(self):
        self.read = True
        db.session.add(self)


class Answer(db.Model):
    """database for QA"""
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q_author_id = db.Column(db.Integer, index=True)
    q_id = db.Column(db.Integer, index=True)
    author = db.Column(db.Integer, index=True)
    app = db.Column(db.Integer, default=0)
    opp = db.Column(db.Integer, default=0)
    adopt = db.Column(db.Boolean(), default=False)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.now)

    def up(self):
        self.app += 1
        db.session.add(self)

    def down(self):
        self.opp += 1
        db.session.add(self)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, index=True)
    clink = db.Column(db.Integer, default=0)
    reply = db.Column(db.Integer, default=0)
    answer = db.Column(db.Boolean(), default=False)
    title = db.Column(db.Text())
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.now)

    @staticmethod
    def changde_reply(target, value, oldvalue, initiator):
        q = Question.query.filter_by(id=value).first()
        q.reply += 1
        db.session.add(q)

    def read(self):
        self.clink += 1
        db.session.add(self)

db.event.listen(Answer.q_id, 'set', Question.changde_reply)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    the_id = db.Column(db.Integer, index=True)
    from_id = db.Column(db.Integer, index=True)
    post_id = db.Column(db.Integer, index=True, nullable=True)
    post_author_id = db.Column(db.Integer, index=True, nullable=True)
    comment_id = db.Column(db.Integer, index=True, nullable=True)
    q_id = db.Column(db.Integer, index=True, nullable=True)
    q_author_id = db.Column(db.Integer, index=True, nullable=True)
    body_id = db.Column(db.Integer, index=True)
    is_read = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime(), default=datetime.now)

    def read(self):
        self.is_read = True
        db.session.add(self)

    def read_all(id):
        ms = Messages.query.filter(
            or_(Messages.the_id == id, Messages.post_author_id == id, Messages.q_author_id == id)).all()
        for m in ms:
            m.is_read = True
            db.session.add(m)
