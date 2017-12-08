# coding = utf-8
# 视图
from flask import render_template, make_response, redirect, url_for, request, flash, abort, g
from datetime import datetime
from . import main
from flask_login import current_user, login_required
from ..models import User, Follow, Topic, Post, TopicFollows, Comments, Messages, Answer, Question
from .forms import UserInfo, UserPasswd, Avatar, TopicForm, PostForm, EditTopic, CommentForm, SearchForm, AskForm
from .. import db
from sqlalchemy import and_, or_
import re

# @main.route('/search/', methods=['GET', 'POST'])
# def Search(sss):
#     # posts = Post.query.filter(Post.body.like(sss)).all()
#     # return render_template('search.html', posts=posts, search=SearchForm(),
#     # Topic=Topic)
#     return redirect(url_for('main.Searchs', xxx=sss))


@main.route('/search/<xxx>', methods=['GET', 'POST'])
def Searchs(xxx):
    sss = '%' + xxx + '%'
    posts = Post.query.filter(
        or_(Post.body.like(sss), Post.head.like(sss))).all()
    return render_template('search.html', posts=posts, search=SearchForm(), Topic=Topic, User=User)


@main.before_app_request
def before_request():
    search = SearchForm()
    if search.validate_on_submit():
        s = search.s.data
        # return Search(s)
        return redirect(url_for('main.Searchs', xxx=s))
    elif current_user.is_authenticated:
        current_user.ping()
        current_user.noread_messages = (Messages.query.filter_by(
            the_id=current_user.id).filter_by(is_read=False).count() + Messages.query.filter_by(
            post_author_id=current_user.id).filter_by(is_read=False).count() + Messages.query.filter_by(
            q_author_id=current_user.id).filter_by(is_read=False).count())
        db.session.add(current_user)


@main.route('/user/seting/', methods=['GET', 'POST'])
@login_required
def user_seting():
    index = request.cookies.get('xx', 'seting1')
    form = UserInfo()
    if index == 'seting1':
        form = UserInfo()
        if form.validate_on_submit():
            current_user.name = form.realname.data
            current_user.location = form.location.data
            current_user.abortme = form.abortme.data
            db.session.add(current_user)
            flash('资料已更新')
            return redirect(url_for('main.info_resp'))
        form.realname.data = current_user.name
        form.location.data = current_user.location
        form.abortme.data = current_user.abortme
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='个人信息', id=id)
    if index == 'seting2':
        form = UserPasswd()
        if form.validate_on_submit():
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('密码已更改')
            return redirect(url_for('main.passwd_resp'))
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='密码设置', id=id)
    if index == 'seting3':
        form = Avatar()
        if form.validate_on_submit():
            img = form.avatar.data
            filename = str(datetime.now()).split(
                '.')[-1] + 'id%d' % current_user.id
            img.save('blog/static/user/avatar/%s.jpg' % filename)
            current_user.avatar = '%s.jpg' % filename
            db.session.add(current_user)
            flash('头像修改成功')
            return redirect(url_for('main.email_resp'))
        # return render_template('index.html', user=current_user, index=index,
        # form=form, title='头像设置', id=id)

    return render_template('index.html', user=current_user, index=index, form=form, title='用户设置', search=SearchForm())


@main.route('/', methods=['GET', 'POST'])
def home():
    # search = Search()
    # if search:
    # return render_template('search.html', posts=search, search=SearchForm(),
    # Topic=Topic)
    return render_template('home.html', user=current_user, search=SearchForm())

# 用户主页


@main.route('/user/<id>')
def user_index(id):
    user = User.query.get_or_404(id)
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    show = 0
    if current_user.is_authenticated():
        show = request.cookies.get('show', '')
    if show_followed == 0:
        pass
    posts = Post.query.filter_by(author=user.id).order_by(Post.timestamp).all()
    return render_template('index.html', user=user, Topic=Topic, posts=posts[::-1], index='index,info', c1=c1, c2=c2, search=SearchForm(), Comments=Comments)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.user_index')))
    resp.set_cookie('show', '0', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/post')
@login_required
def show_post():
    resp = make_response(redirect(url_for('.user_index')))
    resp.set_cookie('show', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/answer')
@login_required
def show_answer():
    resp = make_response(redirect(url_for('.user_index')))
    resp.set_cookie('show', '2', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/comment')
@login_required
def show_comment():
    resp = make_response(redirect(url_for('.user_index')))
    resp.set_cookie('show', '3', max_age=30 * 24 * 60 * 60)
    return resp

# 用户设置


@main.route('/seting/info')
@login_required
def info_resp():
    resp = make_response(redirect(url_for('.user_seting')))
    resp.set_cookie('xx', 'seting1', max_age=60)
    return resp


@main.route('/seting/passwd')
@login_required
def passwd_resp():
    resp = make_response(redirect(url_for('.user_seting')))
    resp.set_cookie('xx', 'seting2', max_age=60)
    return resp


@main.route('/seting/email')
@login_required
def email_resp():
    resp = make_response(redirect(url_for('.user_seting')))
    resp.set_cookie('xx', 'seting3', max_age=60)
    return resp

# 所有关注者界面


@main.route('/user/follower-all/<id>')
def user_follower_all(id):
    user = User.query.get_or_404(id)
    all_follower = user.all_follower()
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    return render_template('index.html', user=user, User=User, index='follower-all,index', all_follower=all_follower, c1=c1, c2=c2, search=SearchForm())

# 所有关注的人界面


@main.route('/user/followed-all/<id>')
def user_followed_all(id):
    user = User.query.get_or_404(id)
    all_followed = user.all_follow()
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    return render_template('index.html', user=user, User=User, index='followed-all,index', all_followed=all_followed, c1=c1, c2=c2, search=SearchForm())

# 关注用户


@main.route('/user/follow/<id>')
@login_required
def user_follow(id):
    user = User.query.get_or_404(id)
    current_user.follow(user)
    flash('关注成功')
    return redirect(url_for('main.user_index', id=user.id))

# 取消关注用户


@main.route('/user/unfollow/<id>')
@login_required
def user_unfollow(id):
    user = User.query.get_or_404(id)
    current_user.unfollow(user)
    flash('已取消关注')
    return redirect(url_for('main.user_index', id=user.id))

# 所有话题


@main.route('/topics', methods=['GET', 'POST'])
def topics():
    topics = Topic.query.all()
    form = TopicForm()
    if current_user.is_authenticated and form.validate_on_submit():
        t = Topic(topic=form.topic_name.data,
                  info=form.topic_info.data, author=current_user.id)
        db.session.add(t)
        img = form.topic_img.data
        img.save('blog/static/topics/%s.jpg' % form.topic_name.data)
        t.img = '%s.jpg' % form.topic_name.data
        db.session.add(t)
        return redirect(url_for('main.topics', form=form, topics=topics))
    return render_template('topics/topics.html', form=form, topics=topics, search=SearchForm(), Post=Post)

# 话题


@main.route('/topics/<topic>', methods=['GET', 'POST'])
def topic(topic):
    form = EditTopic()
    t = Topic.query.filter_by(topic=topic).first()
    if not t:
        abort(404)
    if form.validate_on_submit():
        t.info = form.topic_info.data
        db.session.add(t)
        return redirect(url_for('main.topic', topic=t.topic))
    t.ping()
    form.topic_info.data = t.info
    f = None
    if current_user.is_authenticated:
        f = TopicFollows.is_follow(current_user.id, t.id)
    return render_template('topics/topic.html', t=t, f=f, title=topic, Post=Post, User=User, form=form, search=SearchForm(), Comments=Comments)

# 新帖子


@main.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if Topic.query.all() == []:
        flash('还没有任何主题，添加一个吧。')
        return redirect(url_for('main.topics'))
    if form.validate_on_submit():
        p = Post(author=current_user.id, tpoic=form.topic.data,
                 head=form.head.data, body=form.postbody.data)
        db.session.add(p)
        db.session.commit()
        # p = Post.query.order_by(Post.id).first()[::-1]
        return redirect(url_for('main.post', id=p.id))
    topics = Topic.query.order_by(Topic.id).all()
    return render_template('topics/new_post.html', form=form, title='新帖子', topics=topics, search=SearchForm())


@main.route('/delete-post/<id>')
@login_required
def delete_post(id):
    '''删除帖子'''
    p = Post.query.get_or_404(id)
    topic = Topic.query.filter_by(id=p.tpoic).first().topic
    user = User.query.filter_by(id=p.author).first()
    if user.is_self(current_user):
        db.session.delete(p)
        cs = Comments.query.filter_by(post_id=p.id).all()
        for c in cs:
            db.session.delete(c)
        db.session.commit()
        flash('帖子已删除')
        return redirect(url_for('main.topic', topic=topic))
    else:
        flash('无法删除')
        return redirect(url_for('main.topic', topic=topic))
# 帖子


@main.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    commentform = CommentForm()
    p = Post.query.get_or_404(id)
    if current_user.is_authenticated and commentform.validate_on_submit():
        comment = Comments(author=current_user.id,
                           post_id=p.id, body=commentform.body.data, post_author_id=p.author)
        db.session.add(comment)
        db.session.commit()
        x = re.match('.*@(.+)\s.*', commentform.body.data)
        if x:
            username = x.group(1)
            u = User.query.filter_by(username=username).first()
            if u:
                mes = Messages(post_author_id=p.author, the_id=u.id, from_id=current_user.id,
                               comment_id=p.id, post_id=p.id, body_id=comment.id)
                db.session.add(mes)
        else:
            mes = Messages(post_author_id=p.author, from_id=current_user.id,
                           post_id=p.id, body_id=comment.id)
            db.session.add(mes)
        return redirect(url_for('main.post', id=p.id))
    p.ping()
    topic = Topic.query.filter_by(id=p.tpoic).first().topic
    author = User.query.filter_by(id=p.author).first()
    comments = Comments.query.filter_by(post_id=p.id).all()

    return render_template('topics/post.html', p=p, topic=topic, author=author, commentform=commentform, search=SearchForm(), comments=comments, User=User)


@main.route('/topic/follow/<topic>')
@login_required
def follow_topic(topic):
    t = Topic.query.filter_by(topic=topic).first()
    user = current_user
    TopicFollows.follow(user.id, t.id)
    return redirect(url_for('main.topic', topic=topic))


@main.route('/topic/unfollow/<topic>')
@login_required
def unfollow_topic(topic):
    t = Topic.query.filter_by(topic=topic).first()
    TopicFollows.unfollow(current_user.id, t.id)
    return redirect(url_for('main.topic', topic=topic))


@main.route('/user/messages')
@login_required
def messages():
    # messages = Comments.query.filter_by(
    #     post_author_id=current_user.id).all()[::-1]
    post_ms = Messages.query.filter_by(
        post_author_id=current_user.id).filter_by(is_read=False).all()
    at_ms = Messages.query.filter_by(
        the_id=current_user.id).filter_by(is_read=False).all()
    a_ms = Messages.query.filter_by(
        q_author_id=current_user.id).filter_by(is_read=False).all()
    read_ms = Messages.query.filter_by(is_read=True).all()
    return render_template('user/messages.html', a_ms=a_ms, Question=Question, post_ms=post_ms, at_ms=at_ms, search=SearchForm(), User=User, Post=Post, Comments=Comments, read_ms=read_ms)


@main.route('/user/read_all_messages')
@login_required
def read_all_messages():
    Messages.read_all(current_user.id)
    return redirect(url_for('main.messages'))


@main.route('/user/messages/read/<id>')
@login_required
def read_message(id):
    ms = Messages.query.get_or_404(id)
    ms.read()
    return redirect(url_for('main.post', id=ms.post_id))


@main.route('/user/messagess/read/<id>')
@login_required
def read_messages(id):
    ms = Messages.query.get_or_404(id)
    ms.read()
    return redirect(url_for('main.question', id=ms.q_id))


@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    qs = Question.query.order_by(Question.timestamp).all()
    form = AskForm()
    if form.validate_on_submit():
        q = Question(author=current_user.id,
                     title=form.title.data, body=form.body.data)
        db.session.add(q)
        flash('提问已发布')
        return redirect(url_for('main.ask'))
    return render_template('ask/ask_index.html', search=SearchForm(), qs=qs, form=form, User=User)


@main.route('/sak/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    q = Question.query.get_or_404(id)
    q.read()
    commentform = CommentForm()
    answers = Answer.query.filter_by(q_id=id).all()
    if current_user.is_authenticated and commentform.validate_on_submit():
        a = Answer(q_id=id, q_author_id=q.author,
                   author=current_user.id, body=commentform.body.data)
        db.session.add(a)
        x = re.match('.*@(.+)\s.*', commentform.body.data)
        if x:
            username = x.group(1)
            u = User.query.filter_by(username=username).first()
            if u:
                mes = Messages(q_author_id=q.author, the_id=u.id, from_id=current_user.id,
                               comment_id=q.id, q_id=q.id, body_id=a.id)
                db.session.add(mes)
        else:
            mes = Messages(q_author_id=q.author, from_id=current_user.id,
                           q_id=q.id, body_id=a.id)
            db.session.add(mes)
        return redirect(url_for('main.question', id=id))
    return render_template('ask/question.html', q=q, search=SearchForm(), User=User, commentform=commentform, answers=answers)
