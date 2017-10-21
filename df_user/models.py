from django.db import models
from db.base_model import BaseModel


class PassportManager(models.Manager):
    '''模型管理器类,一个模型类对应一个模型管理器类'''
    def add_one_passport(self, username, password, email):
        models_name = self.model
        obj = models_name(username=username, password=password, email=email)
        obj.save()
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