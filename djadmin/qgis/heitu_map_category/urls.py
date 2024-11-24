from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "heitumapcategory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.HeituMapCategoryListView.as_view(), name='category_list'),
    path('index/', views.index, name='heitu_index'),
    # Retrieve single task object
    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.HeituMapCategoryIndex, name='category_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.HeituMapCategoryDataList, name='category_datalist'),
    # api
    path('create/', views.HeituMapCategoryListView.as_view(), name='category_create'),
    path('', views.HeituMapCategoryList.as_view(), name='category_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.HeituMapCategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.HeituMapCategoryDetail.as_view(), name='category_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.HeituMapCategoryDetail.as_view(), name='category_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
