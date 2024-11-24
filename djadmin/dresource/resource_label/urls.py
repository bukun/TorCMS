from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "resourcelabel"
urlpatterns = [
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.LabelDataList, name='label_datalist'),

    path('create/', views.LabelsList.as_view(), name='label_create'),
    path('', views.LabelsList.as_view(), name='label_list'),
    re_path(r'^(?P<pk>\d+)/$', views.LabelsDetail.as_view(), name='label_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.LabelsDetail.as_view(), name='label_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.LabelsDetail.as_view(), name='label_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
