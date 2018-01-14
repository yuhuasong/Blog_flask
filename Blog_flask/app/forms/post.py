
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('',render_kw={'placeholder':'标题'},validators=[DataRequired(),Length(3,50,message='标题太长了（3~50个字符）')])
    content = TextAreaField('',render_kw={'placeholder':'这一刻的想法...'},validators=[DataRequired(),Length(3,128,message='说话请注意分寸（3~128个字符）')])
    submit = SubmitField('发表')




class ReplyForm(FlaskForm):
    content = TextAreaField('',render_kw={'placeholder':'这一刻的想法...'},validators=[DataRequired(),Length(3,128,message='说话请注意分寸（3~128个字符）')])
    submit = SubmitField('发表')




