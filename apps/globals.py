# -*- coding:utf-8 -*-
from werkzeug.local import LocalStack
from boss_common.core.ctx import LocalContext

_global_ctx_stack = LocalStack()

global_context = LocalContext(_global_ctx_stack)
g = global_context.local_proxy('g')
config = global_context.local_proxy('config')
ums_db = global_context.local_proxy('ums_db')
boss_db = global_context.local_proxy('boss_db')
current_app = global_context.local_proxy('app')
