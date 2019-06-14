import dash
import os
import logging

from shuttle import Shuttle
from flask import send_from_directory
from pymongo import MongoClient

logger = logging.getLogger(__name__)

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css',
        'rel': 'stylesheet',
    }
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)
app.config.supress_callback_exceptions = True


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


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
