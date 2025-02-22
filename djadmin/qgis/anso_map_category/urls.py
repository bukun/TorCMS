from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "ansomapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.ANSOMapCategoryListView.as_view(), name='category_list'),
    path('index/', views.index, name='anso_index'),
    # Retrieve single task object
    re_path(
        r'^list/(?P<pk>[0-9a-zA-Z]+)', views.ANSOMapCategoryIndex, name='category_index'
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.ANSOMapCategoryDataList,
        name='category_datalist',
    ),
    # api
    path('create/', views.ANSOMapCategoryListView.as_view(), name='category_create'),
    path('', views.ANSOMapCategoryList.as_view(), name='category_list'),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.ANSOMapCategoryDetail.as_view(),
        name='category_detail',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/update/$',
        views.ANSOMapCategoryDetail.as_view(),
        name='category_update',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/delete/$',
        views.ANSOMapCategoryDetail.as_view(),
        name='category_delete',
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
