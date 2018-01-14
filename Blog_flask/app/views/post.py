

from flask import Blueprint, flash, redirect, url_for, request, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import PostForm, ReplyForm
from app.models import Post

post = Blueprint('post',__name__)

@post.route('/publish/',methods=['POST','GET'])
def publish():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:

            user = current_user._get_current_object()
            p = Post(content=form.content.data, title=form.title.data,user=user)
            db.session.add(p)
            flash('帖子发表成功')
            return redirect(url_for('post.publish'))
        else:
            flash('登录后才能发表，请先登录')
            return redirect(url_for('user.login'))

    page = request.args.get('page', 1, type=int)
    allpost = Post.query.filter_by(rid=0).order_by(Post.timestamp.desc())
    pagination = allpost.paginate(page, per_page=5, error_out=False)
    posts = pagination.items
    return render_template('post/publish.html', form=form, posts=posts, pagination=pagination)

#我发表的帖子
@post.route('/list/<int:id>')   #id为当前用户的id
def list(id):
    allpost = Post.query.filter_by(uid=id).order_by(Post.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    pagination = allpost.paginate(page, per_page=2, error_out=False)
    posts = pagination.items
    return render_template('post/list.html',posts=posts, pagination=pagination, id=id)


@post.route('/collect/<int:id>')  #id为帖子的id
@login_required
def collect(id):
    post=Post.query.get(id)
    post.click=post.click + 1
    current_user.posts.append(post)
    db.session.add(current_user)
    return redirect(url_for('post.mycollect'))

@post.route('/discollect/<int:id>')  #id为帖子的id
@login_required
def discollect(id):
    post=Post.query.get(id)
    current_user.posts.remove(post)
    db.session.add(current_user)
    return redirect(url_for('post.mycollect'))


#收藏帖子展示
@post.route('/mycollect/')
@login_required
def mycollect():

    postlist =current_user.posts

    return render_template('post/mycollect.html', postlist=postlist)


#查看帖子详情
@post.route('/detail/<int:id>',methods=['POST','GET'])
def detail(id):
    form = ReplyForm()
    page = request.args.get('page',1,type=int)
    post = Post.query.get(id)
    allpost = Post.query.filter_by(rid=id).order_by(Post.timestamp.desc())
    pagination = allpost.paginate(page,per_page=3,error_out=False)
    posts = pagination.items
    if current_user.is_authenticated:
        if form.validate_on_submit():
            user= current_user._get_current_object()
            p = Post(content=form.content.data,rid=id,user=user)
            db.session.add(p)
            flash('帖子回复成功')
            return redirect(url_for('post.detail',id=id))
        return render_template('post/detail.html',pagination=pagination,post=post,id=id,form=form,posts=posts)
    else:
        flash('登陆后才能回复帖子')
        return redirect(url_for('user.login'))
