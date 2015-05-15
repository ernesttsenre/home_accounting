# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_operation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='account',
            field=models.ForeignKey(verbose_name='Счет', related_name='operations', to='money.Account', on_delete='cascade'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='comment',
            field=models.TextField(verbose_name='Комментарий', null=True),
        ),
    ]
