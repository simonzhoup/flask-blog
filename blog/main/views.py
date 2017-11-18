# coding = utf-8
# 视图
from flask import render_template, make_response, redirect, url_for, request
from . import main
from flask_login import current_user, login_required
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    index = request.cookies.get('index', '')
    if index == 'seting':
        return redirect(url_for('main.user_seting_info', info=''))
    return render_template('index.html', user=current_user, index=index)


@main.route('/<index>')
def index_resp(index):
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('index', index, max_age=2)
    return resp


@main.route('/seting/<info>', methods=['GET', 'POST'])
@login_required
def user_seting(info):
    info = request.cookies.get('info', '')
    if not info:
        info = 'info'
    return render_template('index.html', user=current_user, info=info)


@main.route('/seting/<info>')
@login_required
def user_seting_info(info):
    resp = make_response(redirect(url_for('.user_seting')))
    resp.set_cookie('info', info, max_age=2)
    return resp
