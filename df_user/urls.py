from django.conf.urls import include, url
from django.contrib import admin
from df_user import views


urlpatterns = [
    url('^register/$', views.register),
    # url(r'^register_handle/$', views.register_handle),  # 实现用户信息的注册
    url(r'^check_user_exist/$', views.check_user_exist),  # 检查用户是否存在
    url(r'^login/$', views.login),  # 用户登录页
    url(r'^login_check/$', views.login_check),   # 验证登录名是否存在
    url(r'^address/$', views.address),  # 用户中心地址
    url(r'^order/$', views.order),  # 用户中心内订单
    url(r'^$', views.user),  # 用户中心内订单
    url(r'^place/$', views.show_place),  # 展示订单页
    url(r'^logout/$', views.logout),  # 退出登录

]
