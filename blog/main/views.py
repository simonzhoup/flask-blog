# coding = utf-8
# 视图
from flask import render_template, make_response, redirect, url_for, request, flash, abort
from datetime import datetime
from . import main
from flask_login import current_user, login_required
from ..models import User
from .forms import UserInfo, UserPasswd, Avatar
from .. import db


@main.route('/user/seting', methods=['GET', 'POST'])
def index():
    index = request.cookies.get('xx', 'home')
    form = UserInfo()
    if index == 'seting1' and current_user == user:
        form = UserInfo()
        if form.validate_on_submit():
            current_user.name = form.realname.data
            current_user.location = form.location.data
            current_user.abortme = form.abortme.data
            db.session.add(current_user)
            flash('资料已更新')
            return redirect(url_for('main.info_resp'))
        form.realname.data = current_user.name
        form.location.data = current_user.location
        form.abortme.data = current_user.abortme
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='个人信息', id=id)
    if index == 'seting2' and current_user == user:
        form = UserPasswd()
        if form.validate_on_submit():
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('密码已更改')
            return redirect(url_for('main.passwd_resp'))
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='密码设置', id=id)
    if index == 'seting3' and current_user == user:
        form = Avatar()
        if form.validate_on_submit():
            img = form.avatar.data
            filename = str(datetime.now()).split(
                '.')[-1] + 'id%d' % current_user.id
            img.save('blog/static/user/avatar/%s.jpg' % filename)
            current_user.avatar = '%s.jpg' % filename
            db.session.add(current_user)
            flash('头像修改成功')
            return redirect(url_for('main.index'))
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='头像设置', id=id)
    elif 'seting' in index and current_user != user:
        abort(404)
    return render_template('index.html', user=user, index=index, form=form, title='用户设置')


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)


@main.route('/user/<id>')
def user_index(id):
    user = User.query.get_or_404(id)
    return render_template('index.html', user=user)


@main.route('/seting/info')
@login_required
def info_resp():
    resp = make_response(redirect(url_for('.index', id=current_user.id)))
    resp.set_cookie('xx', 'seting1', max_age=60)
    return resp


@main.route('/seting/passwd')
@login_required
def passwd_resp():
    resp = make_response(redirect(url_for('.index', id=current_user.id)))
    resp.set_cookie('xx', 'seting2', max_age=60)
    return resp


@main.route('/seting/email')
@login_required
def email_resp():
    resp = make_response(redirect(url_for('.index', id=current_user.id)))
    resp.set_cookie('xx', 'seting3', max_age=60)
    return resp
