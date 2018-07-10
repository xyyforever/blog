from .main import main
from .user import user
from .posts import posts


# 默认蓝本配置
DEFAULT_BLUEPRINT = (
    # （蓝本，前缀）
    (main, ''),
    (user, '/user'),
    (posts, '/posts'),
)


# 封装函数，注册蓝本
def register_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
