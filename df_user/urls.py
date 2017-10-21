from django.conf.urls import include, url
from django.contrib import admin
from df_user import views


urlpatterns = [
    url('^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),  # 实现用户信息的注册
]
