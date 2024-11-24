from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "crawl_source"
urlpatterns = [
    # Retrieve task list
    path('list/', views.CategoryList.as_view(), name='crawl_source_list'),

    path('index/', views.index, name='crawl_source_index'),
    path('index_en/', views.index_en, name='crawl_source_index_en'),
    # Retrieve single task object

    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.CategoryIndex,
            name='crawl_source_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryDataList,
            name='crawl_source_datalist'),
    re_path(r'^en/(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryDataListEN,
            name='crawl_source_datalist_en'),


    # api
    path('create/', views.CategoryListView.as_view(),
         name='crawl_source_create'),
    path('', views.CategoryList.as_view(), name='crawl_source_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryDetail.as_view(),
            name='crawl_source_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.CategoryDetail.as_view(),
            name='crawl_source_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.CategoryDetail.as_view(),
            name='crawl_source_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
