# -*-coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):  # 程序工厂函数，用来延迟创建程序实例，可创建多个程序实例，形参为配置环境
    app = Flask(__name__)  # 主程序
    app.config.from_object(config[config_name])  # 导入配置
    config[config_name].init_app(app)  # 初始化扩展

    bootstrap.init_app(app)  # 初始化bootstrap
    mail.init_app(app)  # 初始化邮箱
    moment.init_app(app)  # 初始化时间
    db.init_app(app)  # 初始化数据库
    login_manager.init_app(app)  # 初始化登录管理
    pagedown.init_app(app)  # 初始化富文本

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint  # 注册main蓝本
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint  # 注册认证蓝本
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 如果设置了url_prefix这个参数，
    # 那么在templates下面，必须要有对应的blueprint名字的文件夹，URL也会加上这个前缀

    from .api import api as api_blueprint  # 应用编程接口，注册API蓝本
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    return app
