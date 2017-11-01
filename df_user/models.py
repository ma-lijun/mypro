from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash
from db.base_manager import BaseManager


class PassportManager(BaseManager):
    '''模型管理器类,一个模型类对应一个模型管理器类'''

    def add_one_passport(self, username, password, email):
        # 利用抽象的模型管理器基类的方法保存数据
        obj = self.create_one_object(username=username, password=get_hash(password), email=email)
        # 返回对象
        return obj

    def get_one_passport(self, username, password=None):
        # 根据用户名查找账户信息
        try:
            if password is None:
                # 根据用户名查找账户
                obj = self.get_one_object(username=username)
            else:
                # 根据用户名和密码查找账户信息，密码要使用哈希值
                obj = self.get_one_object( password=get_hash(password), username=username)
        except self.model.DoesNotExist:
            obj = None
        return obj


# 账户表
class Passport(BaseModel):
    '''账户模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassportManager()

    class Meta:
        db_table = 's_user_account'


class AddressManager(BaseManager):
    '''模型管理器类'''
    def get_one_address(self, passport_id):
        '''根据用户的passport_id查询其默认收货地址'''
        try:
            # 使用抽象的基类
            addr = self.get_one_object(passport_id=passport_id, is_default=True)
        except self.model.DoesNotExist:
            addr = None
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, recipient_phone,
                        zip_code, is_default):
        '''添加一个收货地址'''
        addr = self.get_one_address(passport_id=passport_id)
        is_default = False
        if addr is None:
            '''没有默认收货地址'''
            is_default = True
        addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name, recipient_addr=recipient_addr
                                      , recipient_phone=recipient_phone, zip_code=zip_code, is_default=is_default)

        return addr


# 地址信息模型类
class Address(BaseModel):
    '''地址信息模型类'''
    recipient_name = models.CharField(max_length=20, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=100, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮编')
    recipient_phone = models.IntegerField(max_length=11, verbose_name='联系电话')
    passport = models.ForeignKey(Passport, verbose_name='所属账户')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'


class BrowseHistoryManager(BaseManager):
    '''
    历史浏览模型管理器类
    '''
    def get_one_history(self, passport_id, goods_id):
        '''
        查询用户是否浏览过某个商品
        '''
        # todo: 代码实现
        browsed = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def add_one_history(self, passport_id, goods_id):
        '''
        添加用户的一条浏览记录
        '''
        # 1.去查找用户是否浏览过该商品 self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        browsed = self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        # 2.如果用户浏览过该商品，则更新update_time，否则插入一条新的浏览记录
        if browsed:
            # 调用browsed.save方法会自动更新update_time
            # print('update')
            browsed.save()
        else:
            browsed = self.create_one_object(passport_id=passport_id, goods_id=goods_id)
        return browsed

    def get_browse_list_by_passport(self, passport_id, limit=None):
        '''
        根据passport_id获取对应用户的浏览记录
        '''
        # 1.根据用户id获取用户的历史浏览记录,browsed_li为一个查询集
        browsed_li = self.get_object_list(filters={'passport_id':passport_id}, order_by=('-update_time',))
        # 2.对查询结果集进行限制
        if limit:
            browsed_li = browsed_li[:limit]
        return browsed_li


class BrowseHistory(BaseModel):
    '''
    历史浏览模型类
    '''
    # todo: 模型类设计
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')

    objects = BrowseHistoryManager()

    class Meta:
        db_table = 's_browse_history'

