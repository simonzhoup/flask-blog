# coding=utf-8
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user, AnonymousUserMixin
from datetime import datetime
from sqlalchemy import and_, or_
from flask import abort, url_for
from functools import wraps
from .exceptions import ValidationError


def admin_required(f):
    @wraps(f)
    def warpper(*args, **kw):
        if not current_user.is_admin():
            abort(404)
        return f(*args, **kw)
    return warpper


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)


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
    administrator = db.Column(db.Boolean(), default=False)
    ban = db.Column(db.Boolean(), default=False)
    # 关系
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref(
        'follower', lazy='joined'), lazy='dynamic', cascade='all,delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref(
        'followed', lazy='joined'), lazy='dynamic', cascade='all,delete-orphan')
    topic = db.relationship('Topic', backref='topic_author', lazy='dynamic')
    post = db.relationship('Post', backref='post_author', lazy='dynamic')
    follow_topic = db.relationship('TopicFollows', backref=db.backref(
        'users', lazy='joined'), lazy='dynamic', cascade='all,delete-orphan')
    comments = db.relationship(
        'Comments', backref='comment_author', lazy='dynamic')
    question = db.relationship(
        'Question', backref='q_author', lazy='dynamic')

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'questions': url_for('api.get_user_questions', id=self.id, _external=True),
            'post_count': self.post.count()
        }
        return json_user

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

    def is_ban(self):
        return self.ban

    def is_admin(self):
        return self.administrator

    def is_self(self, current_user):
        return current_user.is_authenticated and self.id == current_user.id

    def follow(self, user):
        if not self.is_follow(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def all_follow(self):
        return self.followed.all()

    def all_follower(self):
        return self.followers.all()

    def is_follow(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def follow_t(self, topic):
        if not self.is_follow(topic):
            f = TopicFollows(user_id=self.id, topic_id=topic.id)
            db.session.add(f)

    def unfollow_t(self, topic):
        f = TopicFollows.query.filter_by(
            user_id=self.id, topic_id=topic.id).first()
        if f:
            db.session.delete(f)

    def is_follow_t(self, topic):
        return self.follow_topic.filter_by(topic_id=topic.id).first() is not None

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


class AnonymousUser(AnonymousUserMixin):
    '''匿名用户的检查方法'''

    def is_admin(self):
        return False

    def is_self(self, user):
        return False

    def is_ban(self):
        return True


login_manager.anonymous_user = AnonymousUser


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), unique=True, index=True)
    info = db.Column(db.Text())
    img = db.Column(db.String(64), nullable=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    clink = db.Column(db.Integer, default=1)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    activation = db.Column(db.Boolean(), default=True)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')

    def ping(self):
        self.clink += 1
        db.session.add(self)


class TopicFollows(db.Model):
    __tablename__ = 'topicfollows'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey(
        'topics.id'), primary_key=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)


class Comments(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    post_id = db.Column(db.Integer, index=True, nullable=True)
    post_author_id = db.Column(db.Integer, index=True)
    comment_id = db.Column(db.Integer, index=True, nullable=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    read = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    activation = db.Column(db.Boolean(), default=True)

    def read_comment(self):
        self.read = True
        db.session.add(self)

    def to_json(self):
        json_data = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True),
            'author': url_for('api.get_user', id=self.author, _external=True),
            'body': self.body,
            'timestamp': self.timestamp
        }
        return json_data


class Answer(db.Model):
    """database for QA"""
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q_author_id = db.Column(db.Integer, index=True)
    q_id = db.Column(db.Integer, index=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    app = db.Column(db.Integer, default=0)
    opp = db.Column(db.Integer, default=0)
    adopt = db.Column(db.Boolean(), default=False)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    activation = db.Column(db.Boolean(), default=True)

    def up(self):
        self.app += 1
        db.session.add(self)

    def down(self):
        self.opp += 1
        db.session.add(self)

    def to_json(self):
        json_data = {
            'url': url_for('api.get_answer', id=self.id, _external=True),
            'anthor': url_for('api.get_user', id=self.author, _external=True),
            'question': url_for('api.get_question', id=self.q_id, _external=True),
            'agree': self.app,
            'oppose': self.opp,
            'timestamp': self.timestamp,
            'answer': self.body
        }
        return json_data


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    clink = db.Column(db.Integer, default=0)
    reply = db.Column(db.Integer, default=0)
    answer = db.Column(db.Integer)
    title = db.Column(db.Text())
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    activation = db.Column(db.Boolean(), default=True)

    @staticmethod
    def changde_reply(target, value, oldvalue, initiator):
        q = Question.query.filter_by(id=value).first()
        q.reply += 1
        db.session.add(q)

    def read(self):
        self.clink += 1
        db.session.add(self)

    def to_json(self):
        json_data = {
            'url': url_for('api.get_question', id=self.id, _external=True),
            'author': url_for('api.get_user', id=self.author, _external=True),
            'timestamp': self.timestamp,
            'question': self.body,
            'answers': url_for('api.get_question_answers', id=self.id, _external=True)
        }
        return json_data

db.event.listen(Answer.q_id, 'set', Question.changde_reply)


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    the_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    from_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    post_id = db.Column(db.Integer, index=True, nullable=True)
    post_author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), index=True, nullable=True)
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


class PostTag(db.Model):
    __tablename__ = 'posttag'
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), index=True)
    posts = db.relationship('PostTag', foreign_keys=[
                            PostTag.tags_id], backref=db.backref('tag', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    tpoic = db.Column(db.Integer, db.ForeignKey('topics.id'), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    clink = db.Column(db.Integer, default=1)
    head = db.Column(db.String(64))
    body = db.Column(db.Text())
    activation = db.Column(db.Boolean(), default=True)
    tags = db.relationship('PostTag', foreign_keys=[
        PostTag.post_id], backref=db.backref('post', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    def ping(self):
        self.clink += 1
        db.session.add(self)

    def to_json(self):
        json_data = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author, _external=True),
            'comments': url_for('api.get_post_comments', id=self.id, _external=True),
            'comment_count': Comments.query.filter_by(post_id=self.id).count(),
        }
        return json_data

    @staticmethod
    def form_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)
