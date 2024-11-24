from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "farmpro"
urlpatterns = [
    path('create/', views.FarmproDataList.as_view(), name='data_create'),
    path('', views.FarmproDataList.as_view(), name='data_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.FarmproDataDetail.as_view(), name='data_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.FarmproDataDetail.as_view(), name='data_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.FarmproDataDetail.as_view(), name='data_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
