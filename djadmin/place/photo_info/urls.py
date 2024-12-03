from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "photo_info"


urlpatterns = [
    path('create/', views.DataList.as_view(), name='photo_create'),
    path('', views.DataList.as_view(), name='photo_list'),


    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='photo_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='photo_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='photo_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
