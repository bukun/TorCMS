'''
Entry for the application.
'''
import sys
import tornado.ioloop
from config import SITE_CFG
from application import APP_URLS, SETTINGS

PORT = SITE_CFG['PORT']
APP = tornado.web.Application(handlers=APP_URLS, **SETTINGS)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    app = APP
    app.listen(PORT)
    print('Development server is running at http://127.0.0.1:{0}/'.format(PORT))
    print('Quit the server with CONTROL-C')
    tornado.ioloop.IOLoop.instance().start()
