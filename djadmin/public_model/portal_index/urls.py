from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "portal_index"
urlpatterns = [
    path('ydyl/', views.ydyl_index, name='ydyl_index'),  # 中蒙俄协同创新平台 http://ydyl.gislab.cn/

]
urlpatterns = format_suffix_patterns(urlpatterns)