# _*_ coding:utf-8 _*_ 
from django.shortcuts import redirect


def login_requird(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('islogin'):
            # 用户已经登录
            return view_func(request, *args, **kwargs)
        else:
            # 用户未登录
            return redirect('/user/login/')
    return wrapper
