import os
from pathlib import Path
import tornado.ioloop
import tornado.web
from django.core.wsgi import get_wsgi_application
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.wsgi import WSGIContainer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'administor.settings')

django_app = WSGIContainer(
    # django.core.handlers.wsgi.WSGIHandler()
    get_wsgi_application()
)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, Tornado!")

# For Tornado
SETTINGS = {
    "template_path": Path("templates"),
    "static_path": Path(__file__) / 'xx_static',
    # "debug": SITE_CFG["DEBUG"],
    "cookie_secret": 'asdf',
    "login_url": "/user/login",
    # "ui_modules": APP_MODUES,
    # "ui_methods": uifuncs,
}


def make_app():
    return tornado.web.Application([
        # (r"/asdf", MainHandler),
        # (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'xx_static'}),
        (r"/admin/(.*)", FallbackHandler, dict(fallback=django_app)),
        # (r"/portal/(.*)", FallbackHandler, dict(fallback=django_app)),
        # (r"/dataset/(.*)", FallbackHandler, dict(fallback=django_app)),
        # (r"/literature/(.*)", FallbackHandler, dict(fallback=django_app)),
        # (r"/static/(.*)",  FallbackHandler, dict(fallback=django_app)),
        # (r"/(.*)",  FallbackHandler, dict(fallback=django_app)),
    ], **SETTINGS
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(6797)
    print('info')
    tornado.ioloop.IOLoop.current().start()
