from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "wiki"
urlpatterns = [
    path('create/', views.PageList.as_view(), name='page_create'),
    path('', views.PageList.as_view(), name='page_list'),
    re_path(r'^view/(?P<pk>[0-9a-zA-Z]+)/', views.PageDetailView, name='page_view'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.PageDetail.as_view(), name='page_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.PageDetail.as_view(), name='page_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.PageDetail.as_view(), name='page_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
