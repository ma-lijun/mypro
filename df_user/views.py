from django.shortcuts import render, redirect
from df_user.models import Passport


# Create your views here.
def register(request):
    # 显示注册页面
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接受数据
    name = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 保存进数据库
    # passport = Passport(username=name, password=password, email=email)
    # passport.save()
    Passport.objects.add_one_passport(username=name, password=password, email=email)
    # return redirect('/user/register_handle/')
    return redirect('/df_user/login/')


# def register_handle(request):
    # 接受数据
    # name = request.POST.get('name')
    # password =  request.POST.get('password')
    # email = request.POST.get('email')
    # # 保存进数据库
    # passport = Passport(name=name, password=password, email=email)
    # passport.save()
    # return redirect('/user/reg/')
