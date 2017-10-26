# _*_ coding:utf-8 _*_
from django.shortcuts import render, redirect
from df_user.models import Passport, Address
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from df_user.tasks import register_success_send_mail
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from utils.decorators import loginrequied


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
        return redirect('/user/login/')


# def register_handle(request):
#     # 接受数据
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     # 保存进数据库
#     # passport = Passport(username=name, password=password, email=email)
#     # passport.save()
#     # 将保存数据的方法提取到模型管理器类
#     Passport.objects.add_one_passport(username=username, password=password, email=email)
#     # # 3.给用户注册邮箱发邮件
#     # message = '<h1>欢迎您成为天天生鲜注册会员</h1>请记好您的信息:<br/>用户名:'+username+'<br/>密码：'+password
#     # send_mail('欢迎信息', '', settings.EMAIL_FROM, [email], html_message=message)
#     register_success_send_mail.delay(username=username, password=password, email=email)
#     # send_register_success_mail.delay(username=username, password=password, email=email)
#     return redirect('/df_user/login/')


@require_GET
# /user/check_user_exist/   get 方式验证用户名是否存在
def check_user_exist(request):
    # 接收用户
    username = request.GET.get('username')
    # 检查用户名是否存在
    obj = Passport.objects.get_one_passport(username=username)
    if obj:
        res = 0
    else:
        res = 1
    return JsonResponse({'res': res})


# /user/login/
def login(request):
    # 实现记住用户名就能真正显示用户名的后台逻辑
    # 获取cookie   看user是否在其中
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'df_user/login.html', {'username': username})


# /user/login_check/
def login_check(request):
    # 接收用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 查找用户名和密码是否存, 使用命名参数容错能力更强
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # # 判断登录之前的地址是否需要记录
    # if request.session.has_key('pre_url_path'):
    #     next = request.session['pre_url_path']
    # else:
    #     # 首页地址
    #     next = '/'
    # 如果查到， json {'res':1}  如果查不到，返回{'res':0}
    if passport:
        # 判断登录之前的地址是否需要记录， 只有登录成功才会有session记录，之外的session被flush了，所有必须下载登录成功的判断里
        if request.session.has_key('pre_url_path'):
            next = request.session['pre_url_path']
        else:
            # 首页地址
            next = '/'
        # 用户名密码正确
        jres = JsonResponse({'res': 1, 'next': next})
        # 获取是否需要记住用户名  返回结果为字符串类型的 true / false
        remember = request.POST.get('remember')
        if remember == 'true':
            jres.set_cookie('username', username, max_age=14*24*3600)
        # 记录登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        # 登录账户的id
        request.session['passport_id'] = passport.id
        return jres
    else:
        return JsonResponse({'res': 0})


# /user/logout/
def logout(request):
    # 退出登录要删除session信息，否则不能真正的退出
    request.session.flush()
    return render(request, 'df_user/login.html')


# /user/
@loginrequied
def user(request):
    return render(request, 'df_user/user_center_info.html', {'page': 'user'})


# /user/address/
# @require_http_methods['GET','POST']
@loginrequied
def address(request):
    passport_id = request.session['passport_id']
    # 根据用户id获取默认收货地址
    if request.method == 'GET':
        # 获取用户默认收货地址
        addr = Address.objects.get_one_address(passport_id=passport_id)
        return render(request, 'df_user/user_center_site.html', {'page': 'address', 'addr':addr})
    else:
        # 获取前端传递的数据
        recipient_name = request.POST.get('recipient_name')
        recipient_addr = request.POST.get('recipient_addr')
        recipient_phone = request.POST.get('recipient_phone')
        zip_code = request.POST.get('zip_code')
        print(recipient_addr)
        addr = Address.objects.add_one_address(passport_id=passport_id, recipient_name=recipient_name, recipient_addr=recipient_addr,
                                               recipient_phone=recipient_phone, zip_code=zip_code)

        return redirect('/user/address/')


# /user/order/
@loginrequied
def order(request):
    return render(request, 'df_user/user_center_order.html', {'page': 'order'})
