from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "zhongbamapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.ZhongbaMapCategoryListView.as_view(), name='category_list'),
    path('index/', views.index, name='zhongba_index'),
    # Retrieve single task object
    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.ZhongbaMapCategoryIndex, name='category_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.ZhongbaMapCategoryDataList, name='category_datalist'),
    # api
    path('create/', views.ZhongbaMapCategoryListView.as_view(), name='category_create'),
    path('', views.ZhongbaMapCategoryList.as_view(), name='category_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.ZhongbaMapCategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.ZhongbaMapCategoryDetail.as_view(), name='category_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.ZhongbaMapCategoryDetail.as_view(), name='category_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
