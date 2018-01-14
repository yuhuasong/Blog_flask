from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.extensions import db, login_manager


class User(UserMixin,db.Model):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    username = Column(String(32),unique=True)
    password_hash = Column(String(128))
    email = Column(String(64))
    icon = Column(String(64),default='1.jpg')
    confirmed = Column(Boolean,default=False)
    post = db.relationship('Post', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_activate_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires_in)
        return s.dumps({'id':self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return  False
        user = User.query.get(data.get('id'))
        if user is None:
            return False
        if not user.confirmed:
            user.confirmed = True
            db.session.add(user)
        return True
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def check_activate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    id = data.get('id')
    email = data.get('email')

    user = User.query.get(id)
    if user is None:
        return False

    if email:
        user.email = email
        db.session.add(user)

    if not user.confirmed:
        # 没有激活就激活
        user.confirmed = True
        db.session.add(user)
    return True















