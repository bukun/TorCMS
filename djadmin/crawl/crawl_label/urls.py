from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "crawl_label"
urlpatterns = [

    path('index/', views.index, name='crawl_label_index'),
    path('index_en/', views.index_en, name='crawl_label_index_en'),
    # Retrieve single task object

    re_path(r'^list/(?P<pk>[0-9a-zA-Z]+)', views.LabelsIndex, name='crawl_label_index'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.LabelsDataList, name='crawl_label_datalist'),
    re_path(r'^en/(?P<pk>[0-9a-zA-Z]+)/$', views.LabelsDataListEN, name='crawl_label_datalist_en'),

    path('create/', views.LabelsList.as_view(), name='crawl_label_create'),
    path('', views.LabelsList.as_view(), name='crawl_label_list'),
    re_path(r'^(?P<pk>\d+)/$', views.LabelsDetail.as_view(), name='crawl_label_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.LabelsDetail.as_view(), name='crawl_label_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.LabelsDetail.as_view(), name='crawl_label_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
