from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "public_country"
urlpatterns = [
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.CountryDataList, name='country_datalist'),

    path('create/', views.CountryList.as_view(), name='country_create'),
    path('', views.CountryList.as_view(), name='country_list'),
    re_path(r'^(?P<pk>\d+)/$', views.CountryDetail.as_view(), name='country_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.CountryDetail.as_view(), name='country_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.CountryDetail.as_view(), name='country_delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
