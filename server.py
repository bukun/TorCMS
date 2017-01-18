# coding:utf-8

import os
import sys
import config
from urls import urls
import tornado.locale
import tornado.web

from torcms.modules.modef import core_modules

cur_modues = {}

modules = dict(core_modules, **cur_modues)

SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "tmplts"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'debug': True,
    "cookie_secret": config.cookie_secret,
    "login_url": "/user/login",
    'ui_modules': modules,
}

PORT = config.PORT

if __name__ == "__main__":
    tornado.locale.set_default_locale('zh_CN')
    tornado.locale.load_gettext_translations('locale', 'yunsuan')
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    # For different theme.
    if PORT[1] == '1':
        # 形如：  8188, 8199
        SETTINGS['template_path'] = os.path.join(os.path.dirname(__file__), "templates_m")

    application = tornado.web.Application(
        handlers=urls,
        **SETTINGS
    )
    application.listen(PORT)
    print ('Development server is running at http://127.0.0.1:{0}/'.format(PORT))
    print ('Quit the server with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()
