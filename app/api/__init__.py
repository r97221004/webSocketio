# -*- coding: UTF-8 -*-
from flask import Flask, render_template


# from app.api.apiv1 import blueprint as api_v1
from app.handler.auth import jwt_required

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'secret!'


@flask_app.before_request
# @jwt_required()
def before_request():
    pass


@flask_app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@flask_app.route('/demo')
def index():
    return render_template('index.html')


def init():
    # flask_app.register_blueprint(api_v1)

    return flask_app
