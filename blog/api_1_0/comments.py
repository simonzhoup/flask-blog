from . import api
from ..models import Comments
from flask import jsonify
from .authentication import auth


@api.route('/comments/')
@auth.login_required
def get_comments():
    comments = Comments.query.all()
    return jsonify({'comments': [comment.to_json() for comment in comments]})


@api.route('/comments/<int:id>')
@auth.login_required
def get_comment(id):
    comment = Comments.query.get_or_404(id)
    return jsonify(comment.to_json())
