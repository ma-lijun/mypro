from django.db import models


# 定义模型类基类
# 继承 models.Model 的类才是模型类
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        '''说明是抽象模型类基类'''
        abstract = True