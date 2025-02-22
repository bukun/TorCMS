from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "qgismap"
urlpatterns = [
    path('create/', views.QgisMapList.as_view(), name='map_create'),
    path('', views.QgisMapList.as_view(), name='map_list'),
    path(
        'get_heitu_map_list/',
        views.APIGetHeituMapList.as_view(),
        name='get_heitu_map_list',
    ),
    re_path(
        r'^get_label/(?P<pk>[0-9a-zA-Z]+)',
        views.LabelAPIView.as_view(),
        name='get_maplist_by_label',
    ),
    re_path(
        r'^view/(?P<mapid>[0-9a-zA-Z]+)/(?P<category>[0-9a-zA-Z]+)',
        views.QgisMapDetailView,
        name='map_view',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$', views.QgisMapDetail.as_view(), name='map_detail'
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/update/$',
        views.QgisMapDetail.as_view(),
        name='map_update',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/delete/$',
        views.QgisMapDetail.as_view(),
        name='map_delete',
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
