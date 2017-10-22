from django.shortcuts import render, redirect
from df_user.models import Passport
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from df_user.tasks import register_success_send_mail
from django.views.decorators.http import require_GET,require_POST,require_http_methods


# 使用django的内置装饰器功能，显示访问方式,优化register接口设计，删除多余接口register_handle
@require_http_methods(['GET', 'POST'])
def register(request):
    # 显示注册页面
    if request.method == 'GET':
        return render(request, 'df_user/register.html')
    elif request.method == 'POST':
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 将保存数据的方法提取到模型管理器类
        Passport.objects.add_one_passport(username=username, password=password, email=email)
        # # 3.给用户注册邮箱发邮件
        register_success_send_mail.delay(username=username, password=password, email=email)
        return redirect('/df_user/login/')


def register_handle(request):
    # 接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    # 保存进数据库
    # passport = Passport(username=name, password=password, email=email)
    # passport.save()
    # 将保存数据的方法提取到模型管理器类
    Passport.objects.add_one_passport(username=username, password=password, email=email)
    # # 3.给用户注册邮箱发邮件
    # message = '<h1>欢迎您成为天天生鲜注册会员</h1>请记好您的信息:<br/>用户名:'+username+'<br/>密码：'+password
    # send_mail('欢迎信息', '', settings.EMAIL_FROM, [email], html_message=message)
    register_success_send_mail.delay(username=username, password=password, email=email)
    # send_register_success_mail.delay(username=username, password=password, email=email)
    return redirect('/df_user/login/')


@require_GET
# /user/check_user_exist/   get 方式验证用户名是否存在
def check_user_exist(request):
    # 接收用户
    username = request.GET.get('username')
    # 检查用户名是否存在
    obj = Passport.objects.get_one_passport(username=username)
    if obj:
        res=0
    else:
        res=1
    return JsonResponse({'res':res})

