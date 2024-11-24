from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "document"
urlpatterns = [
    path('create/', views.DataList.as_view(), name='doc_create'),
    path('doc_update/', views.DataSpiderUpdate, name='doc_spider_update'),
    path('doc_save/', views.save_doc, name='doc_spider_save'),
    path('', views.DataList.as_view(), name='doc_list'),
    re_path(r'^view/(?P<pk>[0-9a-zA-Z]+)/(?P<category>[0-9a-zA-Z]+)', views.DataDetailView, name='doc_view'),

    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='doc_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='doc_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='doc_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
