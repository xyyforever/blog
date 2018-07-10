from flask import Blueprint, jsonify,request,render_template,redirect,flash,url_for
from flask_login import current_user
from app.models import Posts
from app.forms import ReplyForm
from app.extensions import db
posts = Blueprint('posts', __name__)


@posts.route('/collect/<int:pid>')
def collect(pid):
    # 判断是否已经收藏
    if current_user.is_favorite(pid):
        # 取消收藏
        p = Posts.query.get(pid)
        db.session.add(p)
        current_user.favorites.remove(p)
        return jsonify({'status': '收藏'})
    else:
        # 添加收藏
        p = Posts.query.get(pid)
        db.session.add(p)
        current_user.favorites.append(p)
        return jsonify({'status': '取消收藏'})
# 我的发表
@posts.route('/publish_me/')
def publish_me():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, int)
        pagination = Posts.query.filter(Posts.uid == current_user.id).\
            order_by(Posts.timestamp.desc()).paginate(page,per_page=3,error_out=False)
        posts = pagination.items
    else:
        flash('请先登录。。。')
        return redirect(url_for('user.login'))
    return render_template('main/publish.html', posts=posts, pagination=pagination)

# 我的收藏
@posts.route('/collect_me/')
def collect_me():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, int)
        pagination = current_user.favorites.order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=False)
        posts = pagination.items
    else:
        flash('请先登录...')
        return redirect(url_for('user.login'))
    return render_template('main/collect.html', posts=posts, pagination=pagination)

# 回复博客
@posts.route('/replyblog/')
def replyblog():
    form = ReplyForm()
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
        flash('回复成功')
    return render_template('main/replyblog.html',form = form)