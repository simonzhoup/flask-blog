from . import api
from ..models import Answer
from flask import jsonify
from .authentication import auth


@api.route('/answers/')
@auth.login_required
def get_answers():
    answers = Answer.query.all()
    return jsonify({'answers': [answer.to_json() for answer in answers]})


@api.route('/answers/<int:id>')
@auth.login_required
def get_answer(id):
    answer = Answer.query.get_or_404(id)
    return jsonify(answer.to_json())
