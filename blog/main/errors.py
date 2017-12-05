from flask import render_template
from . import main
from .forms import SearchForm


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', search=SearchForm()), 404


@main.app_errorhandler(500)
def error_500(e):
    return render_template('500.html', search=SearchForm()), 500
