#!/usr/bin/env python
#coding: utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import platform
cur_platform = platform.platform()
if cur_platform.startswith('Linux'):
    sys.path.append('/home/michael/install/py_public')
else:
    sys.path.append('/Users/zuotaoliu/install/py_public')

from tornado.options import define, options
import tornado.web
import tornado.httpserver
import tornado.ioloop
import traceback

from urls import urls
from settings import settings, demo_port

import logging
import logging.config
cur_path = os.path.dirname(__file__)
log_conf_file = os.path.join(cur_path, './conf/log.conf')
logging.config.fileConfig(log_conf_file)
ilog = logging.getLogger('root')

define("port", default=demo_port, help="run one the given port", type=int)

def main():
    try:
        tornado.options.parse_command_line()
        application = tornado.web.Application(urls, **settings)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        tb = traceback.format_exc().replace('\n', '')
        print 'tornado server failed: %s' % (tb)

if __name__ == "__main__":
    main()

