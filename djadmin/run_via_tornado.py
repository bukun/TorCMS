
import os
from pathlib import Path 
import tornado.ioloop
import tornado.web
from django.core.wsgi import get_wsgi_application
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.wsgi import WSGIContainer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


django_app = WSGIContainer(
# django.core.handlers.wsgi.WSGIHandler()
get_wsgi_application()
)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, Tornado!")



SETTINGS = {
    "template_path": Path("templates"),
    "static_path": Path(__file__) / 'xx_static' ,
    # "debug": SITE_CFG["DEBUG"],
    "cookie_secret": 'asdf',
    "login_url": "/user/login",
    # "ui_modules": APP_MODUES,
    # "ui_methods": uifuncs,
}

def make_app():
    return tornado.web.Application([
        (r"/asdf", MainHandler),
        # (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'xx_static'}), 
        (r"/admin/(.*)",  FallbackHandler, dict(fallback=django_app)),
        # (r"/(.*)",  FallbackHandler, dict(fallback=django_app)),
    ], **SETTINGS
                                   )



if __name__ == "__main__":
    app = make_app()
    app.listen(6799)
    print('info')
    tornado.ioloop.IOLoop.current().start()


# tonadoService.py10 

# import os
# from tornado.options import options, define
# from tornado import httpserver
# from tornado.ioloop import IOLoop
# from tornado import wsgi
# from django.core.wsgi import get_wsgi_application
# 
# port = 6795
# projectName = "mysite"
# 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'.format(projectName))
# 
# application = get_wsgi_application()
# define('port', port, type=int)
# 
# if __name__ == '__main__':
#     options.parse_command_line()
#     app = wsgi.WSGIContainer(application)
#     http_server = httpserver.HTTPServer(app, xheaders=True)
#     http_server.listen(options.port)
#     IOLoop.instance().start()
