from django.db import models
from db.base_model import BaseModel
from db.base_manager import BaseManager
from df_goods.enums import *
from tinymce.models import HTMLField


# Create your models here.
class GoodsManager(BaseManager):
    """商品模型管理器类"""
    def get_goods_by_type(self, goods_type_id, limit=None, sort='default'):
        '''根据商品类型id获取商品信息'''
        # 定义一个元组order_by , 指定默认排列顺序
        order_by = ('-pk', )
        if sort == 'new':
            '''查询新品信息'''
            order_by = ('create_time',)
        elif sort == 'hot':
            '''按照商品销量查询商品信息'''
            order_by = ('-goods_sales', )
        elif sort == ('goods_price',):
            # 按照商品价格排序
            order_by = ('goods_price', )

        # get_object_list 中 filters是字典类型， order_by是元组类型
        goods_list = self.get_object_list(filters={'goods_type_id':goods_type_id},order_by=order_by )

        # 根据传入的limit取出查询集中的几条数据
        if limit:
            # 对查询集进行切片
            goods_list = goods_list[:limit]
        return goods_list


class Goods(BaseModel):
    '''商品模型类'''
    # 少写两种类型表
    goods_type_choice = (
        (FRUIT, GOODS_TYPE[FRUIT]), # 元组中第一元素是val, 第二个元素显示的信息
        (SEAFOOD, GOODS_TYPE[SEAFOOD]),
        (MEAT, GOODS_TYPE[MEAT]),
        (EGGS, GOODS_TYPE[EGGS]),
        (VEGETABLES, GOODS_TYPE[VEGETABLES]),
        (FROZEN, GOODS_TYPE[FROZEN])
    )

    goods_status_choice = (
        (ONLINE, GOODS_STATUS[ONLINE]),
        (OFFLINE, GOODS_STATUS[OFFLINE]),
    )
    # 1:新鲜水果 2:海鲜水产 3:猪牛羊肉 4:禽类蛋品 5:新鲜蔬菜 6:速冻食品
    goods_type_id = models.SmallIntegerField(choices=goods_type_choice, default=FRUIT, verbose_name='商品类型')
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=50, verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=
                                      '商品价格')  # 商品价格
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='邮费')
    goods_image = models.ImageField(upload_to='goods', verbose_name=' 商品图片')  # 格式要记住
    goods_info = HTMLField(verbose_name='商品描述')
    goods_stock = models.IntegerField(default=1, verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0, verbose_name='商品销量')
    goods_status = models.IntegerField(choices=goods_status_choice, default=ONLINE, verbose_name='商品状态')
    goods_unite = models.CharField(max_length=20, verbose_name='商品单位')
    objects = GoodsManager()

    class Meta:
        db_table = 's_goods'


