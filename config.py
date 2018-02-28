# -*-coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 配置类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'  # 密钥
    MAIL_SERVER = 'smtp.qq.com'  # 邮箱服务器
    MAIL_PORT = '465'  # 邮箱端口
    # MAIL_USE_TLS = True
    MAIL_USE_SSL = True  # 安全套接岑协议
    MAIL_USERNAME = '1130831892@qq.com'  # 用户名
    MAIL_PASSWORD = 'qugkudslltgffhbh'  # 密码
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'  # 主题前缀
    FLASKY_MAIL_SENDER = '1130831892@qq.com'  # 发送方
    FLASKY_ADMIN = '1130831892@qq.com'  # 管理员邮箱
    SSL_REDIRECT = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 每次请求结束后自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
    SQLALCHEMY_RECORD_QUERIES = True  # 启用记录查询统计数字的功能
    FLASKY_POSTS_PER_PAGE = 20  # 每页条目
    FLASKY_FOLLOWERS_PER_PAGE = 50  # 关注者数目
    FLASKY_COMMENTS_PER_PAGE = 30  # 评论条目
    FLASKY_SLOW_DB_QUERY_TIME = 0.5  # 缓慢查询的阈值

    @staticmethod
    def init_app(app):  # 可以执行对当前环境的配置初始化
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # 如果不指定数据库，则使用的是类似内存数据库的技术，程序关闭后数据消失
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 把错误通过电子邮件发送给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_SSL', None):  # 将TLS改为SSL
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# Heroku平台
class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
