from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "igaiscategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.IgaisCategoryListView.as_view(), name='category_list'),
    # Retrieve single task object
    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.IgaisCategoryIndex, name='category_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.IgaisCategoryDataList, name='category_datalist'),
    # api
    path('create/', views.IgaisCategoryDetail.as_view(), name='category_create'),
    path('', views.IgaisCategoryList.as_view(), name='category_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.IgaisCategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.IgaisCategoryDetail.as_view(), name='category_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.IgaisCategoryDetail.as_view(), name='category_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
