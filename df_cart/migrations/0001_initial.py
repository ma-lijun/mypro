# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_user', '0002_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('goods_count', models.IntegerField(verbose_name='商品数目', default=1)),
                ('goods_id', models.ForeignKey(verbose_name='商品ID', to='df_goods.Goods')),
                ('passport_id', models.ForeignKey(verbose_name='账户ID', to='df_user.Passport')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
