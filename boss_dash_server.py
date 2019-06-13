# -*- coding:utf-8 -*-
import logging.config

logging.config.fileConfig('logging_config.ini')

from gevent import monkey

monkey.patch_all()

from apps.dash_bootstrap import bootstrap_boss_dash_app

dash_app = bootstrap_boss_dash_app()

if __name__ == '__main__':
    dash_app.run()
