from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "map"
urlpatterns = [
    path('create/', views.MapList.as_view(), name='map_create'),
    path('', views.MapList.as_view(), name='map_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.MapDetail.as_view(), name='map_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.MapDetail.as_view(), name='map_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.MapDetail.as_view(), name='map_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
