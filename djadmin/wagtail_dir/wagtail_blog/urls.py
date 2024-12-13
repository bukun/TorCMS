from django.urls import path
from . import views

urlpatterns = [
    # ... 其他Wagtail的路由模式 ...

    # 自定义路由
    path('', views.my_custom_view, name='blog_index'),
]