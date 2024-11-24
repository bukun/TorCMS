from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "world"
urlpatterns = [

]
urlpatterns = format_suffix_patterns(urlpatterns)
