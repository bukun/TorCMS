from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "crawl_document_en"
urlpatterns = [
    path('create/', views.DataList.as_view(), name='crawldoc_en_create'),
    path('compare/', views.compare_content, name='crawldoc_en_compare'),

    path('', views.DataList.as_view(), name='crawldoc_en_list'),
    re_path(r'^view/(?P<dataid>[0-9a-zA-Z]+)/', views.DataDetailView, name='crawldoc_en_view'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='crawldoc_en_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='crawldoc_en_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='crawldoc_en_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
