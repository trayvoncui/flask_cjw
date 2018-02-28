# -*-coding:utf-8 -*-
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='1130831892@qq.com',
    MAIL_PASSWORD='qugkudslltgffhbh'
)

mail = Mail(app)


@app.route('/')
def index():
    msg = Message(subject="mongo", sender='1130831892@qq.com', recipients=['512979440@qq.com'])
    msg.html = '<h1>hello world！</h1>'
    mail.send(msg)
    return "hello_world"


if __name__ == '__main__':
    app.run()
