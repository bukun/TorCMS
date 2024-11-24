from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "planar_features"


urlpatterns = [
    path('create/', views.DataList.as_view(), name='data_create'),
    path('', views.DataList.as_view(), name='data_list'),


    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='data_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='data_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='data_delete'),
    path('ajax/load_cities/<str:region>', views.ajax_load_cities, name='load_cities'),

    path('map_view/', views.map_view, name='map_view'),
    path('get_city/<lat>/<lng>/', views.get_city, name='get_city'),
    path('get_by_id/<id>/', views.get_by_id, name='get_by_id'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
