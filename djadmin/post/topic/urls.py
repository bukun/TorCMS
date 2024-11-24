from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "topic"
urlpatterns = [
    path('create/', views.DataList.as_view(), name='topic_create'),

    path('', views.DataList.as_view(), name='topic_list'),
    path('index/', views.index),

    re_path(r'^view/(?P<pk>[0-9a-zA-Z]+)', views.DataDetailView, name='topic_view'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/$', views.DataDetail.as_view(), name='topic_detail'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/update/$', views.DataDetail.as_view(), name='topic_update'),
    re_path(r'^(?P<pk>[0-9a-zA-Z]+)/delete/$', views.DataDetail.as_view(), name='topic_delete'),
    path('sub_comment/', views.comment_control, name='topic_comment'),
    # # 已有代码，处理一级回复

    path('comment/<int:article_id>', views.post_comment, name='post_comment'),
    # 新增代码，处理二级回复
    path('comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')

]
urlpatterns = format_suffix_patterns(urlpatterns)
