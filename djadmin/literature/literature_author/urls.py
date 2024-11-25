from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "literature_author"
urlpatterns = [
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.LabelDataList, name='author_datalist'),

    path('create/', views.LabelsList.as_view(), name='author_create'),
    path('', views.LabelsList.as_view(), name='author_list'),
    re_path(r'^(?P<pk>\d+)/$', views.LabelsDetail.as_view(), name='author_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.LabelsDetail.as_view(), name='author_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.LabelsDetail.as_view(), name='author_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
