from django.shortcuts import render
from df_goods.models import Goods
from df_goods.enums import *

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
