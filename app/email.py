from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail
from threading import Thread


def async_send_mail(app, msg):
    # 邮件发送需要程序上下文，新的线程没有，需要手动创建
    with app.app_context():
        mail.send(msg)


# 封装函数发送邮件
def send_mail(subject, to, template, **kwargs):
    # 从代理中获取原始的应用实例
    app = current_app._get_current_object()
    # 创建邮件消息对象
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(template, **kwargs)
    # 发送邮件
    # 创建异步发送邮件的线程
    thr = Thread(target=async_send_mail, args=(app, msg))
    # 启动线程
    thr.start()
    return thr
