from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "geofea"
urlpatterns = [
    path('create/', views.DataDetail.as_view(), name='data_create'),
    path('', views.DataList.as_view(), name='data_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='data_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='data_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='data_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)