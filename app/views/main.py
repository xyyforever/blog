from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.forms import PostsForm
from app.models import Posts
from flask_login import current_user
from app.extensions import db


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # 获取当前登录用户对象
            user = current_user._get_current_object()
            # 创建对象
            p = Posts(content=form.content.data, user=user)
            # 保存到数据库
            db.session.add(p)
            flash('发表成功')
            return redirect(url_for('main.index'))
        else:
            flash('请登录后再发表')
            return redirect(url_for('user.login'))
    # 查询博客
    # posts = Posts.query.filter(Posts.rid == 0).order_by(Posts.timestamp.desc())
    # 分页查询
    page = request.args.get('page', 1, int)
    pagination = Posts.query.order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)