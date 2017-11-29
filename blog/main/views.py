# coding = utf-8
# 视图
from flask import render_template, make_response, redirect, url_for, request, flash, abort
from datetime import datetime
from . import main
from flask_login import current_user, login_required
from ..models import User, Follow, Topic, Post
from .forms import UserInfo, UserPasswd, Avatar, TopicForm, PostForm
from .. import db

# 用户设置路由


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

    return render_template('index.html', user=current_user, index=index, form=form, title='用户设置')


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)


@main.route('/user/<id>')
def user_index(id):
    user = User.query.get_or_404(id)
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    posts = Post.query.filter_by(author=user.id).order_by(Post.timestamp).all()
    return render_template('index.html', user=user,posts=posts[::-1], index='index,info', c1=c1, c2=c2, title=user.username + '的主页')

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


@main.route('/user/follower-all/<id>')
def user_follower_all(id):
    user = User.query.get_or_404(id)
    all_follower = user.all_follower()
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    return render_template('index.html', user=user, User=User, index='follower-all,index', all_follower=all_follower, c1=c1, c2=c2)


@main.route('/user/followed-all/<id>')
def user_followed_all(id):
    user = User.query.get_or_404(id)
    all_followed = user.all_follow()
    c1 = Follow.query.filter_by(follower_id=user.id).count()
    c2 = Follow.query.filter_by(followed_id=user.id).count()
    return render_template('index.html', user=user, User=User, index='followed-all,index', all_followed=all_followed, c1=c1, c2=c2)


@main.route('/user/follow/<id>')
@login_required
def user_follow(id):
    user = User.query.get_or_404(id)
    current_user.follow(user)
    flash('关注成功')
    return redirect(url_for('main.user_index', id=user.id))


@main.route('/user/unfollow/<id>')
@login_required
def user_unfollow(id):
    user = User.query.get_or_404(id)
    current_user.unfollow(user)
    flash('已取消关注')
    return redirect(url_for('main.user_index', id=user.id))


@main.route('/topics', methods=['GET', 'POST'])
@login_required
def topics():
    topics = Topic.query.all()
    form = TopicForm()
    if form.validate_on_submit():
        t = Topic(topic=form.topic_name.data, info=form.topic_info.data)
        db.session.add(t)
        img = form.topic_img.data
        img.save('blog/static/topics/%s.jpg' % t.id)
        t.img = '%s.jpg' % t.topic
        db.session.add(t)
        return redirect(url_for('main.topics', form=form, topics=topics, title='话题广场'))
    return render_template('topics/topics.html', form=form, topics=topics, title='话题广场')


@main.route('/topics/<topic>')
def topic(topic):
    t = Topic.query.filter_by(topic=topic).first()
    if not t:
        abort(404)
    t.ping()
    return render_template('topics/topic.html', t=t, title=topic)


@main.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(author=current_user.id,tpoic=form.topic.data,head=form.head.data,body=form.body.data)
        db.session.add(p)
        return redirect(url_for('main.topics'))
    return render_template('topics/new_post.html', form=form, title='新帖子')
