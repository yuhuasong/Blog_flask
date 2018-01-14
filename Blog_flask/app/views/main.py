from flask import Blueprint, render_template

from app.email import send_mail

main = Blueprint('main',__name__)



@main.route('/')
def index():
    return render_template('main/index.html')



@main.route('/mail/')
def send():
    send_mail('1454605360@qq.com','关于密码','email/activate',username='xiaoming')
    return 'send mail'












