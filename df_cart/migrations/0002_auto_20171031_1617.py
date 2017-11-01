# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='goods_id',
            new_name='goods',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='passport_id',
            new_name='passport',
        ),
    ]
