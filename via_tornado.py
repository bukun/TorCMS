import os
import tornado.ioloop
import tornado.web
from django.core.wsgi import get_wsgi_application
from tornado.web import FallbackHandler
from tornado.wsgi import WSGIContainer

from application import APP_URLS, SETTINGS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'administor.settings')

'''
以下设置是为了兼容django的异步操作：
```
    SynchronousOnlyOperation at /admin/login/ 
    You cannot call this from an async context - use a thread or sync_to_async.
```
'''
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

def make_app():
    '''
    注意 admin 静态文件的位置，由 TorCMS 的 admin 静态文件位置决定.
    '''
    django_app = WSGIContainer(get_wsgi_application())
    djngo_handler = [
        # Use admin in Django instead of Tornado.
        (r"/admin/(.*)", FallbackHandler, dict(fallback=django_app)),
    ]

    return tornado.web.Application(handlers=djngo_handler + APP_URLS, **SETTINGS)


if __name__ == "__main__":
    app = make_app()
    app.listen(6797)
    print('info')
    tornado.ioloop.IOLoop.current().start()
