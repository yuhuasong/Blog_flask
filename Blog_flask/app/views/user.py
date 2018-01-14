import os

from PIL import Image
from flask import Blueprint, redirect, url_for, render_template, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required

from app.extensions import db, photos
from app.forms import RegisterForm
from app.forms.user import LoginForm, IconForm, EditForm, EmailForm
from app.models.user import User
from app.email import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

user = Blueprint('user',__name__)


@user.route('/register/',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username =form.username.data,password = form.password.data,email = form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_activate_token()
        send_mail(form.email.data,'用户激活','email/activate',token=token,username = user.username)
        flash('注册成功，请去邮箱激活')
        return redirect(url_for('main.index'))
    return render_template('user/registered.html',form = form)


@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


@user.route('/login/',methods=['POST','GET'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user.verify_password(password):
            login_user(user = user,remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('重新登录')
            return redirect(url_for('user.login'))

    return render_template('user/login.html',form=form)


@user.route('/profile/')
def profile():
    return render_template('user/profile.html')

@user.route('/logout/')
def logout():
    logout_user()
    flash('用户已退出登录')
    return redirect(url_for('main.index'))

#修改密码
@user.route('/edit/',methods=['GET','POST'])
@login_required  #保护路由，只有登录后才能修改密码
def edit():
    form = EditForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash("密码修改成功，请重新登录")
            logout_user()
            return redirect(url_for('user.login'))
        else:
            flash('初始密码错误，请重新输入')
            return redirect(url_for('user.edit'))
    return  render_template('user/edit.html',form=form)

#修改邮箱
@user.route('/email/',methods=['GET','POST'])
@login_required
def email():
    form = EmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            s = Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
            token = s.dumps({'id':current_user.id,'email':form.email.data})
            send_mail(form.email.data, '账户激活', 'email/activate', token=token, username=current_user.username)
            flash('激活邮件已经发送到您的邮箱%s，请激活后再登录'%form.email.data)
            return redirect(url_for('user.logout'))
        else:
            flash('密码错误，请重新输入')
            return redirect(url_for('user.email'))
    return render_template('user/email.html',form=form)





@user.route('/icon/',methods = ['POST','GET'])
def icon():
    form = IconForm()
    if form.validate_on_submit():
        suffix = os.path.splitext(form.photo.data.filename)[1]
        name = str(current_user.id) +  random_str() + suffix
        photos.save(form.photo.data,name=name)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],name)
        img = Image.open(pathname)
        img.thumbnail((64,64))
        img.save(pathname)
        if current_user.icon!='1.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        current_user.icon = name
        db.session.add(current_user)
        flash('图像上传成功')
    return render_template('user/icon.html',form=form)

def random_str(length=4):
    import random
    base_str = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join(random.choice(base_str) for i in range(length))













