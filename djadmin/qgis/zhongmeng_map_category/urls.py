from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "zhongmengmapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.ZhongmengMapCategoryListView.as_view(), name='category_list'),
    path('index/', views.index, name='zhongmeng_index'),
    # Retrieve single task object
    re_path(
        r'^list/(?P<pk>[0-9a-zA-Z]+)',
        views.ZhongmengMapCategoryIndex,
        name='category_index',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.ZhongmengMapCategoryDataList,
        name='category_datalist',
    ),
    # api
    path(
        'create/', views.ZhongmengMapCategoryListView.as_view(), name='category_create'
    ),
    path('', views.ZhongmengMapCategoryList.as_view(), name='category_list'),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$',
        views.ZhongmengMapCategoryDetail.as_view(),
        name='category_detail',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/update/$',
        views.ZhongmengMapCategoryDetail.as_view(),
        name='category_update',
    ),
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/delete/$',
        views.ZhongmengMapCategoryDetail.as_view(),
        name='category_delete',
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
