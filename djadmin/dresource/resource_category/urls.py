from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "resourcecatagory"
urlpatterns = [
    # Retrieve task list
    path('list/', views.CategoryList.as_view(), name='category_list'),

    path('index/', views.index, name='resource_category_index'),
    # Retrieve single task object
    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.CategoryIndex, name='category_index'),

    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryDataList, name='category_datalist'),
    # api
    path('create/', views.CategoryListView.as_view(), name='category_create'),
    path('', views.CategoryList.as_view(), name='category_list'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryDetail.as_view(), name='category_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.CategoryDetail.as_view(), name='category_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.CategoryDetail.as_view(), name='category_delete'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
