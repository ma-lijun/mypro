from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from utils.decorators import login_requird
from df_cart.models import Cart

# Create your views here.

# def # /cart/add/?goods_id=商品id&goods_count=商品数目
@require_GET
@login_requird
def cart_add(request):
    '''添加商品到购物车'''
    # 1.获取商品的id和商品数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 2.添加商品的购物车
    res = Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id,
                                   goods_count=int(goods_count))
    print(res)
    # 3.判断res返回json数据
    if res:
        # 添加成功
        return JsonResponse({'res': 1})
    else:
        # 库存不足
        return JsonResponse({'res': 0})


@login_requird
@require_GET
def cart_count(request):
    '''獲取購物車中商品數目'''
    passport_id = request.session.get('passport_id')
    res = Cart.objects.get_court_count_by_passport_id(passport_id=passport_id)
    return JsonResponse({'res': res})


@login_requird
def cart_show(request):
    '''显示购物车页面'''
    passport_id = request.session.get('passport_id')
    # 1.获取用户购物车信息 get_cart_list_by_passport(self, passport_id)
    cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'df_cart/cart.html', {'cart_list': cart_list})


# /cart/del/?goods_id=goods_id
@login_requird
def cart_del(request):
    '''删除购物车记录'''
    # 获取商品和账户信息
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    # 根据商品id 和 账户id 删除购物车记录 Cart.objects.del_cart_info()
    res = Cart.objects.del_cart_info(goods_id, passport_id)
    if res:
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


@require_GET
@login_requird
def cart_update(request):
    '''更新购物车信息'''
    # 1.接收goods_id和goods_count
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    print(goods_id, goods_count, passport_id)
    # 2.更新购物车中商品的信息
    res = Cart.objects.update_cart_info(passport_id=passport_id, goods_id=goods_id, goods_count=int(goods_count))
    # 3.判断res并返回json数据
    if res:
        # 更新成功
        return JsonResponse({'res':1})
    else:
        # 更新失败
        return JsonResponse({'res':0})