from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "qgis_label"
urlpatterns = [
    re_path(
        r'^(?P<pk>[0-9a-zA-Z]+)/$', views.LabelDataList, name='qgis_label_datalist'
    ),
    path('create/', views.LabelsList.as_view(), name='qgis_label_create'),
    path('', views.LabelsList.as_view(), name='qgis_label_list'),
    re_path(r'^(?P<pk>\d+)/$', views.LabelsDetail.as_view(), name='qgis_label_detail'),
    re_path(
        r'^(?P<pk>\d+)/update/$', views.LabelsDetail.as_view(), name='qgis_label_update'
    ),
    re_path(
        r'^(?P<pk>\d+)/delete/$', views.LabelsDetail.as_view(), name='qgis_label_delete'
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
