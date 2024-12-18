from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "jupyter_data"
urlpatterns = [
    path('create/', views.DataList.as_view(), name='data_create'),
    path('index/', views.Index, name='jupyter_index'),
    path('system_index/', views.SystemIndex, name='jupyter_system_index'),
    path('system_index_v2/', views.SystemIndex_v2, name='jupyter_system_index_v2'),
    path('open_dc_system/', views.OpenDCSystem, name='jupyter_open_dc_system'),
    path('open_system/', views.OpenSystem, name='jupyter_open_system'),
    path('', views.DataList.as_view(), name='data_list'),
    re_path(r'^show_share', views.ShowShare, name='share_list'),
    re_path(r'^view/(?P<dataid>[0-9a-zA-Z]+)/', views.DataDetailView, name='data_view'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='data_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='data_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='data_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
