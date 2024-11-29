from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "literature_date"
urlpatterns = [
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.LabelDataList, name='date_datalist'),

    path('create/', views.LabelsList.as_view(), name='date_create'),
    path('', views.LabelsList.as_view(), name='date_list'),
    re_path(r'^(?P<pk>\d+)/$', views.LabelsDetail.as_view(), name='date_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.LabelsDetail.as_view(), name='date_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.LabelsDetail.as_view(), name='date_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
