from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash


class PassportManager(models.Manager):
    '''模型管理器类,一个模型类对应一个模型管理器类'''
    def add_one_passport(self, username, password, email):
        # 获取self所在的模型类

        models_name = self.model
        # 创建一个类对象
        # print(password)
        print(get_hash(password),'1')
        obj = models_name(username=username, password=get_hash(password), email=email)

        # 保存进入数据库
        obj.save()
        # 返回对象
        return obj

    def get_one_passport(self, username):
        # 根据用户名查找账户信息
        try:
            obj = self.get(username=username)
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