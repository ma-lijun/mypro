from django.db import models
from db.base_manager import BaseManager
from db.base_model import BaseModel
# Create your models here.


class CartManager(BaseManager):
    pass


class Cart(BaseModel):
    passport_id = models.ForeignKey('df_user.Passport', verbose_name='账户ID')
    goods_id = models.ForeignKey('df_goods.Goods', verbose_name='商品ID')
    goods_count = models.IntegerField(default=1, verbose_name='商品数目')

    object = CartManager()

    class Meta:
        db_table = 's_cart'
