from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from ..models import admin_required, User, Post, Comments, Question, Topic
from ..main.forms import ManageSearch
from . import manage
from .. import db
from sqlalchemy import and_, or_


@manage.route('/')
@admin_required
def index():
    users = User.query.order_by(User.last_seen).limit(3).all()
    posts = Post.query.order_by(Post.timestamp).limit(3).all()
    questions = Question.query.order_by(Question.timestamp).limit(3).all()
    comments = Comments.query.order_by(Comments.timestamp).limit(3).all()
    return render_template('manage/manage-index.html', info='status', users=users[::-1], posts=posts[::-1],
                           Comments=Comments, questions=questions[::-1], comments=comments[::-1])


@manage.route('/user',methods=['GET','POST'])
@admin_required
def manage_user():
    s = ManageSearch()
    ids = request.args.get('view', 'n')
    if s.validate_on_submit():
        key = s.key.data
        ids = 's'
        users = User.query.filter_by(username=key).all()
    elif ids == 'n':
        users = User.query.order_by(User.last_seen).filter_by(ban=True).all()
    elif ids == 'd':
        users = User.query.order_by(User.last_seen).filter_by(ban=False).all()
    return render_template('manage/manage-user.html', info='user', users=users, User=User, ids=ids, s=ManageSearch())


@manage.route('/user/delete')
@admin_required
def delete_user():
    ids = request.args.get('ids')
    users = ids.split(',')
    for user in users:
        u = User.query.filter_by(username=user).first()
        u.ban = False
        db.session.add(u)
    return redirect(url_for('manage.manage_user'))


@manage.route('/user/undelete')
@admin_required
def undelete_user():
    ids = request.args.get('ids')
    users = ids.split(',')
    for user in users:
        u = User.query.filter_by(username=user).first()
        u.ban = True
        db.session.add(u)
    return redirect(url_for('manage.manage_user'))


@manage.route('/topic', methods=['GET', 'POST'])
@admin_required
def manage_topic():
    s = ManageSearch()
    ids = request.args.get('view', 'n')
    if s.validate_on_submit():
        key = s.key.data
        ids = 's'
        topics = Topic.query.filter(or_(Topic.topic.like(
            key), Topic.info.like(key))).order_by(Topic.timestamp).all()
    elif ids == 'n':
        topics = Topic.query.order_by(
            Topic.timestamp).filter_by(activation=True).all()
    elif ids == 'd':
        topics = Topic.query.order_by(
            Topic.timestamp).filter_by(activation=False).all()
    return render_template('manage/manage_topic.html', info='topic', topics=topics, ids=ids, s=ManageSearch())


@manage.route('/topic/delete')
@admin_required
def delete_topic():
    ids = request.args.get('ids')
    topics = ids.split(',')
    print(topics)
    for topic in topics:
        t = Topic.query.filter_by(id=int(topic)).first()
        t.activation = False
        db.session.add(t)
    return redirect(url_for('manage.manage_topic'))


@manage.route('/topic/undelete')
@admin_required
def undelete_topic():
    ids = request.args.get('ids')
    topics = ids.split(',')
    for topic in topics:
        t = Topic.query.filter_by(id=int(topic)).first()
        t.activation = True
        db.session.add(t)
    return redirect(url_for('manage.manage_topic'))
