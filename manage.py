# -*-coding:utf-8 -*-
# 启动脚本
import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click  # 快速创建命令行
from app import create_app, db
from app.models import User, Role, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():  # shell命令上下文
    return dict(app=app, db=db, User=User, Role=Role, Follow=Follow, Comment=Comment)


manager.add_command("shell", Shell(make_context=make_shell_context))  # 集成Python shell
manager.add_command('db', MigrateCommand)


@manager.command
# @click.option('--coverage/--no-coverage', default=False,
#               help='Run tests under code coverage.')
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):  # 用git中的代码报错：WindowsError: [Error 193] %1 不是有效的 Win32。改用课本的
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


# 在请求分析器的监视下运行程序
@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


# 部署命令
@manager.command
def deploy():
    """Run deployment tasks."""
    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有用户都关注此用户
    User.add_self_follows()


if __name__ == '__main__':
    app.run()
