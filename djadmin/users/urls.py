from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "users"
urlpatterns = [
    path('create/', views.UserList.as_view(), name='user_create'),
    path('register_api/', views.RegisterAPIveiw.as_view(), name='user_register'),
    path('get_userinfo/', views.GetUserInfo.as_view(), name='user_get_userinfo'),
    path('change_user_password/', views.change_user_password.as_view(), name='user_change_user_password'),
    path('update_user/', views.UpdateUserAPIveiw.as_view(), name='user_update_user'),
    re_path(r'^treelist', views.grouplist, name='group_list'),
    # path('', views.UserList.as_view(), name='user_list'),
    re_path(r'^group/', views.GroupList.as_view(), name='group_list'),
    re_path(r'^(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user_detail'),
    re_path(r'^(?P<pk>\d+)/update/$', views.UserDetail.as_view(), name='user_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.UserDetail.as_view(), name='user_delete'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.user_profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
