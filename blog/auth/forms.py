# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import User


class UserRegister(FlaskForm):
    username = StringField(u'用户名：', validators=[Required(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9]*$', 0, 'Usernames must have only letters,numbers,')])
    email = StringField(u'邮箱：', validators=[
                        Required(), Email(), Length(1, 64)])
    password = PasswordField(
        u'密码：', validators=[Required(), EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(u'确认密码：', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'此邮箱已经注册过了'	)


class UserLogin(FlaskForm):
    email = StringField(u'邮箱：', validators=[
                        Required(), Email(), Length(1, 64)])
    password = StringField(
        u'密码：', validators=[Required(), Length(1, 64)])
    submit = SubmitField(u'登录')
