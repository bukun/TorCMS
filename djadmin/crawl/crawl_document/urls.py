from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "crawl_document"
urlpatterns = [
    path('create/', views.DataList.as_view(), name='crawl_doc_create'),
    path('', views.DataList.as_view(), name='crawl_doc_list'),
    re_path(r'^view/(?P<dataid>[0-9a-zA-Z]+)/', views.DataDetailView, name='crawl_doc_view'),

    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='crawl_doc_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='crawl_doc_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='crawl_doc_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
