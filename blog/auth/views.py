from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import UserRegister, UserLogin
from ..models import User
from .. import db
from flask_login import login_user, login_required, logout_user


@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegister()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        return redirect(url_for('main.index'))
    return render_template('user/user_register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    form = UserLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            user.ping()
            flash(u'登录成功')
            return redirect(url_for('main.home'))
        flash('Invalid username or password.')
    return render_template('user/user_login.html', form=form)


@auth.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))
