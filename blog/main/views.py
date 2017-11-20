# coding = utf-8
# 视图
from flask import render_template, make_response, redirect, url_for, request, flash
from . import main
from flask_login import current_user, login_required
from ..models import User
from .forms import UserInfo, UserPasswd
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    index = request.cookies.get('xx', 'home')
    if index == 'seting1' and current_user.is_authenticated:
        form = UserInfo()
        if form.validate_on_submit():
            current_user.name = form.realname.data
            current_user.location = form.location.data
            current_user.abortme = form.abortme.data
            db.session.add(current_user)
            flash('资料已更新')
            return redirect(url_for('main.index'))
        form.realname.data = current_user.name
        form.location.data = current_user.location
        form.abortme.data = current_user.abortme
        return render_template('index.html', user=current_user, index=index, form=form)
    if index == 'seting2' and current_user.is_authenticated:
        form = UserPasswd()
        if form.validate_on_submit():
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('密码已更改')
            return redirect(url_for('main.index'))
        return render_template('index.html', user=current_user, index=index, form=form)
    if index == 'seting3' and current_user.is_authenticated:
        form = UserPasswd()
        return render_template('index.html', user=current_user, index=index, form=form)
    else:
        return render_template('index.html', user=current_user, index=index)


@main.route('/home/')
@login_required
def home_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'home')
    return resp


@main.route('/index/')
@login_required
def index_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'index')
    return resp


@main.route('/seting/')
@login_required
def seting_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'seting1', max_age=60)
    return resp


@main.route('/seting/info')
@login_required
def info_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'seting1', max_age=60)
    return resp


@main.route('/seting/passwd')
@login_required
def passwd_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'seting2', max_age=60)
    return resp


@main.route('/seting/email')
@login_required
def email_resp():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('xx', 'seting3', max_age=60)
    return resp
