from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from ..models import admin_required, User, Post, Comments, Question
from . import manage
from .. import db


@manage.route('/')
@admin_required
def index():
    users = User.query.order_by(User.last_seen).limit(3).all()
    posts = Post.query.order_by(Post.timestamp).limit(3).all()
    questions = Question.query.order_by(Question.timestamp).limit(3).all()
    comments = Comments.query.order_by(Comments.timestamp).limit(3).all()
    return render_template('manage/manage-index.html', info='status', users=users[::-1], posts=posts[::-1],
                           Comments=Comments, questions=questions[::-1], comments=comments[::-1])


@manage.route('/user')
@admin_required
def manage_user():
    ids = request.args.get('view', 'n')
    if ids == 'n':
        users = User.query.order_by(User.last_seen).filter_by(ban=True).all()
    elif ids == 'd':
        users = User.query.order_by(User.last_seen).filter_by(ban=False).all()
    return render_template('manage/manage-user.html', info='user', users=users, User=User, ids=ids)


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
