# _*_ coding:utf-8 _*_ 
from django.db import models
import copy


class BaseManager(models.Manager):
    '''抽象模型管理器基类'''

    def get_all_valid_fields(self):
        # 获取模型类所有的有效字段列表
        model_class = self.model
        # 获取属性元组
        fields_tuple = model_class._meta.get_fields()
        # 保存字段列表
        fields_str_list = []
        for field in fields_tuple:
            if isinstance(field, models.ForeignKey):
                field_name = '%s_id' % field.name
            else:
                field_name = field.name
            # 自己在这个地方做错了一次
            fields_str_list.append(field_name)
        return fields_str_list

    def get_one_object(self, **filters):
        # 根据filters查询
        try:
            obj = self.get(**filters)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def create_one_object(self, **filters):
        # 验证有效文本域
        # 获取模型类的有效属性列表
        valid_fields = self.get_all_valid_fields()
        # 拷贝keywords
        kwd = copy.copy(filters)
        # 去除filters中不在valid_fields中的元素
        for k in kwd:
            if k not in valid_fields:
                filters.pop(k)

        # 新增元素
        model_class = self.model
        obj = model_class(**filters)
        obj.save()
        return obj

