# _*_ coding:utf-8 _*_ 
from django.conf.urls import include, url
from django.contrib import admin
from df_goods import views

urlpatterns = [
    url(r'^$', views.home_list_page),  # 显示首页

]

