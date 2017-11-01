from django.shortcuts import render
from df_goods.models import Goods, Image
from df_goods.enums import *
from django.core.paginator import Paginator
from df_user.models import BrowseHistory

# Create your views here.


# //
def home_list_page(request):
    # 根据默认查询排序查询水平信息4个， 新品查出3个
    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=3, sort='new')

    seafood = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafood_new = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')

    meat = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meat_new = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=3, sort='new')

    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=3, sort='new')

    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=3, sort='new')

    frozen = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozen_new = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=3, sort='new')
    # 组织上下文
    context = {
        'fruits': fruits, 'fruits_new': fruits_new,
        'seafood': seafood, 'seafood_new': seafood_new,
        'meat': meat, 'meat_new': meat_new,
        'eggs': eggs, 'eggs_new': eggs_new,
        'vegetables': vegetables, 'vegetables_new': vegetables_new,
        'frozen': frozen, 'frozen_new': frozen_new,
    }
    return render(request, 'df_goods/index.html', context)


def goods_detail(request, goods_id):

    """
        # 方法一：
    # 根据商品id获取商品信息
    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    # 根据商品类型查询新品信息
    # 根据商品id查询出一张商品的详情图片
    images = Image.objects.get_image_by_goods_id(goods_id=goods_id)
    
        # 方法二：
    # 利用一种办法将商品和图片的查询放到商品的一个方法中
    goods = Goods.objects.get_goods_by_id_with_image(goods_id=goods_id)
    """
    # 方法三：
    # 为商品增加一个同名的可以查询商品和图片的方法，起一个不同的管理器类名
    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # 3.获取商品类型标题
    type_title = GOODS_TYPE[goods.goods_type_id]
    if request.session.has_key('islogin'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=goods_id)
    return render(request,'df_goods/detail.html', {'goods': goods, 'goods_new': goods_new, 'type_title': type_title})


def goods_list(request, goods_type_id, pindex):
    print(request.path)
    '''商品列表页展示'''
    # 获取商品的排序方式
    sort = request.GET.get('sort', 'default')
    # 商品列表
    goods_li = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort=sort)
    # 查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort='new', limit=2)
    # # 进行分页   错误的用法
    # paginator = Paginator.page(goods_li, 1)


    # 进行分页
    paginator = Paginator(goods_li, 2)
    # 取第pindex页的内容
    pindex = int(pindex)
    goods_li = paginator.page(pindex)
    # todo: 进行页码控制
    # 获取总页数
    num_pages = paginator.num_pages
    '''
    0.如果不足5页,显示全部页码
    1.当前页是前三页,显示1-5页
    2.当前页是后三页,显示后5页
    3.既不
    '''
    if num_pages < 5:
        pages = range(1, num_pages+1)
    elif pindex <= 3:
        pages = range(1, 6)
    elif num_pages - pindex <= 2:
        pages = range(num_pages-4, num_pages+1)
    else:
        pages = range(pindex - 2, pindex+3)

    return render(request, 'df_goods/list.html', {'goods_li': goods_li,
                                                  'goods_new': goods_new,
                                                  'type_id': goods_type_id,
                                                  "sort": sort,
                                                  'type-title': GOODS_TYPE[int(goods_type_id)],
                                                  'pages': pages})











