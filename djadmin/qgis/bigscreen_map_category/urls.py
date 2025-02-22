from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "bigscreenmapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.BigScreenMapCategoryListView.as_view(), name='category_list'),
    path('index/', views.index, name='bigscreen_index'),
    # Retrieve single task object
    re_path(
        r'^list/(?P<pk>[0-9a-zA-Z]+)',
        views.BigScreenMapCategoryIndex,
        name='category_index',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.BigScreenMapCategoryDataList,
        name='category_datalist',
    ),
    # api
    path(
        'create/', views.BigScreenMapCategoryListView.as_view(), name='category_create'
    ),
    path('', views.BigScreenMapCategoryList.as_view(), name='category_list'),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.BigScreenMapCategoryDetail.as_view(),
        name='category_detail',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/update/$',
        views.BigScreenMapCategoryDetail.as_view(),
        name='category_update',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/delete/$',
        views.BigScreenMapCategoryDetail.as_view(),
        name='category_delete',
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
