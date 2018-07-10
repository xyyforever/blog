from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import photos


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(6, 10, '用户名必须在6~10个字符之间')])
    password = PasswordField('密码', validators=[Length(6, 18, '密码长度必须在6~18个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', '两次密码不一致')])
    email = StringField('邮箱', validators=[Email('邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 用户名邮箱需要添加自定义验证函数

# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')

# 上传头像表单
class UploadForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired('请选择上传文件'), FileAllowed(photos, '只能上传图片文件')])
    submit = SubmitField('立即上传')


# 发表博客表单
class PostsForm(FlaskForm):
    # 设置标签属性可以通过render_kw参数完成
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'},validators=[Length(3, 120, '内容必须在3~120个字符之间')])
    submit = SubmitField('发表')

# 评论博客表单
class ReplyForm(FlaskForm):
    # 设置标签属性可以通过render_kw参数完成
    content = TextAreaField('', render_kw={'placeholder': '回复内容。。。'},validators=[Length(3, 120, '内容必须在3~120个字符之间')])
    submit = SubmitField('回复')

# 修改密码的表单
class AlterPwdForm(FlaskForm):
    oldpwd = PasswordField('旧密码', validators=[DataRequired('密码不能为空')])
    newpwd = PasswordField('新密码', validators=[DataRequired('密码不能为空')])
    re_newpwd = PasswordField('确认新密码', validators=[EqualTo('newpwd','两次密码不一致')])
    submit = SubmitField('修改')