from _datetime import datetime

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

from app.extensions import db

user_posts = db.Table(
    'user_post',
    Column('user_id',Integer,db.ForeignKey('users.id')),
    Column('post_id',Integer,db.ForeignKey('posts.id')),
)


class Post(db.Model):
    __tablename__='posts'
    id = Column(Integer,primary_key=True)
    rid = Column(Integer,index=True,default=0)
    title = Column(Text)
    content = Column(Text)
    click = Column(Integer,default=0)
    timestamp = Column(DateTime,default=datetime.utcnow)

    users = db.relationship('User',backref = 'posts',secondary = user_posts,lazy='dynamic')

    uid = db.Column(Integer,ForeignKey('users.id'))






