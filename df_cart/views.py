from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from utils.decorators import login_requird

# Create your views here.

# def # /cart/add/?goods_id=商品id&goods_count=商品数目
@require_GET
@login_requird
def cart_add(request):
    '''添加商品到购物车'''
    # # 1.获取商品的id和商品数目
    # goods_id = request.GET.get('goods_id')
    # goods_count = request.GET.get('goods_count')
    # passport_id = request.session.get('passport_id')
    # # 2.添加商品的购物车
    # res = Cart.objects.add_one_cart_info(passport_id=passport_id, goods_id=goods_id,
    #                                goods_count=int(goods_count))
    # # 3.判断res返回json数据
    # if res:
    #     # 添加成功
    #     return JsonResponse({'res':1})
    # else:
    #     # 库存不足
    #     return JsonResponse({'res':0})
    return JsonResponse({'res': 1})
