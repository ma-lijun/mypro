from django.db import models
from db.base_manager import BaseManager
from db.base_model import BaseModel
from df_goods.models import Goods
from django.db.models import Sum
# Create your models here.


class CartManager(BaseManager):
    '''購物車模型管理器類'''
    def get_one_cart_info(self,  passport_id, goods_id):
        # 根據賬戶和商品id查詢購物車中是否有記錄
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self, passport_id, goods_id, goods_count):
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        if cart_info:
            # 購物車商品已經存在添加
            total_count = cart_info.goods_count + goods_count
            if total_count <= goods.goods_stock:
                # 添加成功
                cart_info.goods_count = total_count
                cart_info.save()
                return True
            else:
                # 添加失敗
                return False
        else:
            # 購物車改商品不存在，新增記錄
            # 判斷庫存是否充足
            if goods_count <= goods.goods_stock:
                cart_info = self.create_one_object(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
                return True
            else:
                return False

    def get_court_count_by_passport_id(self, passport_id):
        '''根據用戶id獲取購物車中商品數目'''
        # 若使用mysql查詢
        # select sum(goods_count) from s_cart where passport_id=passport_id
        res_dict = self.filter(passport_id=passport_id).aggregate(Sum('goods_count'))  # {'goods_count__sum':结果}
        if res_dict is None:
            res = 0
        else:
            res = res_dict['goods_count__sum']
        return res

    def get_cart_list_by_passport(self, passport_id):
        '''查询用户购物车记录信息'''
        cart_list = self.get_object_list(filters={'passport_id':passport_id})
        return cart_list

    def del_cart_info(self,goods_id, passport_id):
        '''删除购物车记录'''
        goods_info = self.get_one_cart_info(goods_id=goods_id, passport_id=passport_id)
        try:
            goods_info.delete()
            return True
        except:
            return False

    def update_cart_info(self, passport_id, goods_id, goods_count):
        '''更新购物车记录信息'''
        cart_info = self.get_one_cart_info(passport_id=passport_id, goods_id=goods_id)
        print(cart_info)
        if goods_count <= cart_info.goods.goods_stock:
            # 库存充足
            cart_info.goods_count = goods_count
            cart_info.save()
            return True
        else:
            # 库存不足
            return False

    def get_cart_list_by_id_list(self, cart_id_list):
        '''查询购物车记录信息'''
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        # self.filter(id__in = cart_id_list)
        return cart_list

class Cart(BaseModel):
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户名稱')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品名稱')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'
