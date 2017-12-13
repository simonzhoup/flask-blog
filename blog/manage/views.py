from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models import admin_required
from . import manage


@manage.route('/')
@admin_required
def manage():
    return '<h1>Hello World!</h1>'
