from flask import Flask
from app.config import config
from app.extensions import config_extensions
from app.views import register_blueprint


# 书写工厂函数创建应用实例
def create_app(config_name):
    # 创建用于实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config.get(config_name, 'default'))
    # 配置扩展
    config_extensions(app)
    # 注册蓝本
    register_blueprint(app)
    # 返回应用实例
    return app
