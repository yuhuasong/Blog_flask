from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from app.extensions import photos
from app.models.user import User


class RegisterForm(FlaskForm):
    username = StringField('请输入用户名',validators=[DataRequired(),Length(2,18,message='用户名字符长度为2~18位')])
    password = PasswordField('请输入密码',validators=[DataRequired(),Length(2,12,message='密码字符长度位2~12位')])
    confirm = PasswordField('请再次输入密码',validators=[EqualTo('password',message='两次密码不一致')])
    email = StringField('请输入邮箱',validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self,field):
        if not User.query.filter_by(username = field.data).first():
            raise ValidationError('该用户名已存在，请使用其他用户名')

class IconForm(FlaskForm):
    photo = FileField('上传图片',validators=[FileRequired('请选择文件'),FileAllowed(photos,'只能上传图片')])
    submit = SubmitField('立即上传')

class EditForm(FlaskForm):
    password = PasswordField('请输入初始密码', validators=[DataRequired()])
    newpassword = PasswordField('请输入新密码', validators=[DataRequired(), Length(6, 20, message='密码为6-20个字符')])
    confirm = PasswordField('请再次输入密码', validators=[DataRequired(), EqualTo('newpassword', message='两次密码不一致')])
    submit = SubmitField('提交')

class EmailForm(FlaskForm):
    password = PasswordField('请输入密码', validators=[DataRequired()])
    email = StringField('新的邮箱',validators=[DataRequired(),Length(1,60),Email(message='邮箱格式不正确')])
    summit = SubmitField('确定')











