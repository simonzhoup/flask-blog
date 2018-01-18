from . import api
from ..models import Question, Answer
from flask import jsonify
from .authentication import auth


@api.route('/questions/')
@auth.login_required
def get_questions():
    questions = Question.query.all()
    return jsonify({'questions': [question.to_json() for question in questions]})


@api.route('/questions/<int:id>')
@auth.login_required
def get_question(id):
    question = Question.query.get_or_404(id)
    return jsonify({'question': question.to_json()})


@api.route('/questions/<int:id>/answers')
@auth.login_required
def get_question_answers(id):
    question = Question.query.get_or_404(id)
    answers = Answer.query.filter_by(q_id=id).all()
    return jsonify({'answers': [answer.to_json() for answer in answers]})
