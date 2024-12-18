# settings.py
WAGTAIL_SITE_NAME = 'WAGTAIL ADMIN'
# # 允许的主机
# ALLOWED_HOSTS = ['your-wagtail-host.com', 'localhost']

# 在你的 Wagtail 设置中设置独立的主机和端口
# WAGTAIL_WORKER_PORT = 23456  # 你想要的端口号
WAGTAIL_WORKER_HOST = 'https://cms.igadc.cn/wagtail_cms/'  # 你的独立主机
WAGTAILADMIN_BASE_URL = 'your-custom-admin-url/'
#
# # 为 Wagtail 设置自定义的登录和导航模板
# WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'myapp/login.html'
# WAGTAIL_FRONTEND_NAVIGATION_TEMPLATE = 'myapp/navigation.html'
#
# # 在 urls.py 中定义 Wagtail 的路由和静态文件服务
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include
# from wagtail.admin import urls as wagtailadmin_urls
# from wagtail.core import urls as wagtail_urls
# from wagtail.documents import urls as wagtaildocs_urls
#
# urlpatterns = [
#     path('admin/', include(wagtailadmin_urls)),
#     path('documents/', include(wagtaildocs_urls)),
#     path('', include(wagtail_urls)),
#     # ... 其他 Django 或者 Wagtail 的 URL 模式 ...
# ]
#
# # 如果你的环境设置了 DEBUG 模式，并且你想要为 Wagtail 提供静态文件服务，可以添加下面的代码
# if settings.DEBUG:
#     from django.views.static import serve
#
#     urlpatterns += [
#         path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
#         path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
#     ]

