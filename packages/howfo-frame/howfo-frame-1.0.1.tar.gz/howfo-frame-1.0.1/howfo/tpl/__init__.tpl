# -*- coding: utf-8 -*-
"""
    howfo.base
    Implements various base.
    :copyright: 2019 Kalaiya86
    :license: MIT License
"""

import os
from flask import Flask
from flask.helpers import get_env
from flask_sqlalchemy import SQLAlchemy

from howfo.config import config, config_dict
from howfo.logger import create_logger
from .helpers import base_path

db = SQLAlchemy()


def create_app(config_env):
    project_root_path = base_path(config_dict.get("url_prefix"))
    app = Flask(__name__, static_url_path=config_dict.get("url_prefix") + '/static', static_folder="static", template_folder="app/templates",root_path=project_root_path)
    # 读入 flask config 对象
    app.config.update(config_dict.get('app'))

    db.init_app(app)
    db.app = app

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 注册蓝本
    # 增加auth蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # 附加路由和自定义的错误页面

    return app


# 初始化 flask app
config_env = get_env()
app = create_app(config_env)
log = create_logger(app)
