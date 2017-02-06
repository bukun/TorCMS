# coding:utf-8

import sys
from config import SITE_CFG
import tornado.ioloop

# import tornado.web

PORT = SITE_CFG['PORT']

from application import app

if __name__ == "__main__":
    # tornado.locale.set_default_locale('zh_CN')
    # tornado.locale.load_gettext_translations('locale', 'yunsuan')
    if len(sys.argv) > 1:
        PORT = sys.argv[1]

    app.listen(PORT)
    print('Development server is running at http://127.0.0.1:{0}/'.format(PORT))
    print('Quit the server with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()
