from app.extensions import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,current_user
from datetime import datetime


# 用户模型类
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(20))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=True)
    # 添加保存头像文件名的字段
    icon = db.Column(db.String(64), default='default.jpg')
    # 添加博客的反向引用
    posts = db.relationship('Posts', lazy='dynamic', backref='user')
    # 添加收藏的反向引用
    favorites = db.relationship('Posts', lazy='dynamic', secondary='collections', backref=db.backref('users', lazy='dynamic'))

    # 判断是否收藏
    def is_favorite(self, pid):
        favorite = self.favorites.filter(Posts.id == pid).first()
        if favorite:
            return True
        return False

    # 属性函数
    @property
    def password(self):
        raise AttributeError('密码属性不可读')

    # 设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码校验
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成账户激活的token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    # 账户激活token的检验
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            # 根据用户名查找数据库
            u = User.query.get(data['id'])
            # 查看用户是否激活
            if not u.confirmed:
                # 若没有激活，激活用户
                u.confirmed = True
                db.session.add(u)
            return True
        except:
            return False


# 博客模型
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加外键关联
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))


# 用户收藏博客关联表
collections = db.Table('collections',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'))
)


# 添加回调函数
@login_manager.user_loader
def user_loader(uid):
    return User.query.get(uid)
