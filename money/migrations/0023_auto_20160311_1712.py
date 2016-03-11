# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0022_auto_20150608_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='account',
            field=models.ForeignKey(verbose_name='Счет', related_query_name='operations', related_name='operations', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='category',
            field=models.ForeignKey(verbose_name='Основание', blank=True, related_name='operations', null=True, to='money.Category'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='transfer',
            field=models.ForeignKey(verbose_name='Перевод', editable=False, blank=True, related_name='operations', null=True, to='money.Transfer'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='user',
            field=models.ForeignKey(verbose_name='Пользователь', related_name='operations', to=settings.AUTH_USER_MODEL),
        ),
    ]
