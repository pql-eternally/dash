# -*- coding: utf-8 -*-

import logging
import dash_core_components as dcc
import dash_html_components as html

from pymongo import MongoClient
from shuttle import Shuttle
from dash.dependencies import Input, Output

from apps import staff_app, bill_app, personal_bill_app
from apps.app import app


logger = logging.getLogger(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/staff':
        return staff_app.layout
    elif pathname == '/apps/bill':
        return bill_app.layout
    elif pathname == '/apps/personal_bill':
        return personal_bill_app.layout
    else:
        return '404 Not Found'


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


def run(app, env_var='DASH_APP_CFG', config_yaml='boss_dash.example.yml', app_cls=None):
    shuttle = Shuttle()
    if config_yaml:
        logger.info('loading default config from %s', config_yaml)
        shuttle.config.from_yaml_file(config_yaml, True)
    if env_var:
        logger.info('loading config from ENV:%s', env_var)
        shuttle.config.from_env_var(env_var, True)
    config = shuttle.config
    ums_db = init_mongo_db(config, 'ums_db')
    boss_db = init_mongo_db(config, 'boss_db')
    qlife_db = init_mongo_db(config, 'qlife_db')
    app.custom_config = config
    app.ums_db = ums_db
    app.boss_db = boss_db
    app.qlife_db = qlife_db

    host = config.wsgi.get('host', '127.0.0.1')
    port = config.wsgi.get('port', 8050)
    debug = config.wsgi.get('debug', True)
    app.run_server(port=port, debug=debug)


if __name__ == '__main__':
    run(app)
