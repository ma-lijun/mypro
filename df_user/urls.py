from django.conf.urls import include, url
from django.contrib import admin
from df_user import views


urlpatterns = [
    url('^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),  # 实现用户信息的注册
    url(r'^check_user_exist/$', views.check_user_exist),  # 检查用户是否存在
]
