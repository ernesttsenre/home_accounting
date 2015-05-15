# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('money', '0004_auto_20150513_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='user',
            field=models.ForeignKey(default=1, verbose_name='Пользователь', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
