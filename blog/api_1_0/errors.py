from . import api
from ..exceptions import ValidationError
from flask import jsonify


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@api.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'Notfound', 'message': 'Page Not Found'})
    response.status_code = 404
    return response


@api.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'Internal server error',
                        'message': 'Internal server error'})
    response.status_code = 500
    return response
