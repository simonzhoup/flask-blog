from . import api
from ..models import User, Answer, Comments, Post, Question
from flask import jsonify
from .authentication import auth


@api.route('/')
@auth.login_required
def get_index():
    users = User.query.all()
    posts = Post.query.all()
    comments = Comments.query.all()
    questions = Question.query.all()
    answers = Answer.query.all()
    return jsonify({
        'users': [user.to_json() for user in users],
        'posts': [post.to_json() for post in posts],
        'comments': [comment.to_json() for comment in comments],
        'questions': [question.to_json() for question in questions],
        'answers': [answer.to_json() for answer in answers],
    })


@api.route('/users/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
@auth.login_required
def get_user_posts(id):
    user = User.query.get_or_404(id)
    posts = user.post
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/users/<int:id>/questions/')
@auth.login_required
def get_user_questions(id):
    user = User.query.get_or_404(id)
    questions = user.question
    return jsonify({'questions': [question.to_json() for question in questions]})
