from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "yaoumapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.YaouMapCategoryListView.as_view(), name='category_list'),
    path('sindex/', views.index, name='sindex'), #https://cms.igadc.cn/ 首页
    path('index/', views.yaou_index, name='yaou_index'), #亚欧首页
    path('map_index/', views.map_index, name='map_index'), #地图首页
    path('', views.big_index, name='big_index'), #地图首页
    # Retrieve single task object
    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.YaouMapCategoryIndex, name='category_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.YaouMapCategoryDataList, name='category_datalist'),
    # api
    path('create/', views.YaouMapCategoryListView.as_view(), name='category_create'),
    path('', views.YaouMapCategoryList.as_view(), name='category_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.YaouMapCategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.YaouMapCategoryDetail.as_view(), name='category_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.YaouMapCategoryDetail.as_view(), name='category_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
