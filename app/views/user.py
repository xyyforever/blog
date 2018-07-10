from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app
from app.forms import RegisterForm, LoginForm, UploadForm, AlterPwdForm
from app.email import send_mail
from app.models import User
from app.extensions import db, photos
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
import os


user = Blueprint('user', __name__)


# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 创建用户对象
        u = User()
        try:
            u.username = form.username.data
            u.password = form.password.data
            u.email = form.email.data
        except Exception as e:
            flash('用户名或邮箱不可用')
            return redirect(url_for('user.register'))
        # 保存到数据库
        db.session.add(u)
        # 手动提交，因为生成token时需要使用用户id
        db.session.commit()
        # 生成包含有效信息的token
        token = u.generate_activate_token()
        # 发送激活邮件
        send_mail('账户激活', form.email.data, 'email/activate.html', token=token)
        flash('注册成功，请点击邮件中的链接以完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


# 用户激活
@user.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('user.login'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 根据用户名查找数据库
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash('请先激活，然后再登录')
        elif u.verify_password(form.password.data):
            # 用户登录
            login_user(u, remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)


# 退出登录
@user.route('/logout/')
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


# 用户详情
@user.route('/profile/')
# 保护路由，需要登录才能访问
@login_required
def profile():
    return render_template('user/profile.html')


# 修改头像
@user.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = UploadForm()
    if form.validate_on_submit():
        # 提取后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 生成随机文件名
        filename = random_string() + suffix
        # 保存上传文件
        photos.save(form.icon.data, name=filename)
        # 拼接完整文件路径名
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 生成缩略图
        img = Image.open(pathname)
        # 设置尺寸
        img.thumbnail((64, 64))
        # 覆盖保存图片
        img.save(pathname)
        # 删除原来的头像（默认头像除外）
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存到数据库
        current_user.icon = filename
        db.session.add(current_user)
    # 获取url
    img_url = url_for('static', filename='upload/'+current_user.icon)
    return render_template('user/icon.html', form=form, img_url=img_url)
# 修改密码
@user.route('/alter_pwd/',methods = ['GET','POST'])
def alter_pwd():
    form = AlterPwdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpwd.data):
            current_user.password = form.newpwd.data
            db.session.add(current_user)
            flash('密码修改成功，请重新登录')
            return redirect(url_for('user.login'))
        else:
            flash('旧密码有误')
    return render_template('user/alterpwd.html',form = form)

# 生成随机字符串
def random_string(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))
