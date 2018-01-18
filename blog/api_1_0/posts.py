from . import api
from ..models import Post, Comments
from flask import jsonify
from .authentication import auth


@api.route('/posts/')
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/posts/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@auth.login_required
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user.id
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('apt.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/posts/<int:id>/comments')
@auth.login_required
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    comments = Comments.query.filter_by(post_id=id).all()
    return jsonify({'comments': [comment.to_json() for comment in comments]})
