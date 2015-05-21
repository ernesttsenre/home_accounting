# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('money', '0009_auto_20150520_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='user',
            field=models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operation',
            name='category',
            field=models.ForeignKey(verbose_name='Основание', blank=True, to='money.Category', null=True),
        ),
    ]
