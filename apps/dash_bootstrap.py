# -*- coding:utf-8 -*-
import logging
import flask

from flask import render_template, redirect
from shuttle import Shuttle
from pymongo import MongoClient
from boss_common.core.globals import global_context
from boss_common.core.ctx import _AppCtxGlobals
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from aoao_boss_app import app as boss_app
from ums_app import app as ums_app


flask_app = flask.Flask(__name__)
logger = logging.getLogger(__name__)

application = DispatcherMiddleware(flask_app, {
    '/boss': boss_app.server,
    '/ums': ums_app.server,
})


@flask_app.route('/')
def index():
    return redirect('/boss/')

#
# app.layout = html.Div([
#     dcc.Tabs(
#         id="tabs",
#         value='boss',
#         children=[
#             dcc.Tab(label='嗷嗷Boss', value='boss'),
#             dcc.Tab(label='BossUms', value='ums'),
#             dcc.Tab(label='Boss老板', value='qlife'),
#         ]
#     ),
#     html.Div(id='tabs-content')
# ])


def init_mongo_db(config, db_key):
    if not config:
        return

    mongodb_service = config.get('mongodb_service', {})
    mongo_config = mongodb_service.get(db_key, {})
    if not mongo_config:
        logger.info('init mongo <%s> fail, not found config', db_key)
        return

    db_uri = mongo_config.get('uri', '')
    database = mongo_config.get('database', '')
    if not db_uri or not database:
        logger.info('init mongo <%s> fail, not found config', db_key)
        return

    conn = MongoClient(db_uri)
    mongo_db = conn[db_key]
    logger.info('register and conn %s success', db_key)
    return mongo_db


def boss_dash_app_load_config(config):
    """Initialize seaguard application context.

    This will invoke when shuttle core registered all resources, before accept first request.

    :param app:
    :type app: shuttle.Shuttle
    :return:
    :rtype:
    """

    ums_db = init_mongo_db(config, 'ums_db')
    boss_db = init_mongo_db(config, 'boss_db')
    qlife_db = init_mongo_db(config, 'qlife_db')
    global_context.g = _AppCtxGlobals()
    global_context.config = config
    global_context.ums_db = ums_db
    global_context.boss_db = boss_db
    global_context.qlife_db = qlife_db
    global_context.push()


def run(config):
    host = config.wsgi.get('host', '127.0.0.1')
    port = config.wsgi.get('port', 8050)
    debug = config.wsgi.get('debug', True)
    run_simple(host, port, application)


def bootstrap_boss_dash_app(env_var='DASH_APP_CFG', config_yaml='boss_dash.example.yml', app_cls=None):
    shuttle = Shuttle()
    if config_yaml:
        logger.info('loading default config from %s', config_yaml)
        shuttle.config.from_yaml_file(config_yaml, True)
    if env_var:
        logger.info('loading config from ENV:%s', env_var)
        shuttle.config.from_env_var(env_var, True)
    config = shuttle.config

    boss_dash_app_load_config(config)
    flask_app.run = run(config)
    return flask_app
