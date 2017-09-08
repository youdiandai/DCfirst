#-*- encoding:utf-8 -*-
from flask import Flask,render_template,session,make_response,send_file,request
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
mail = Mail()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #附加路由和自定义的错误页面

    return app