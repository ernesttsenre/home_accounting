# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 10, 35, 49, 707507, tzinfo=utc), verbose_name='Создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 10, 36, 13, 798857, tzinfo=utc), verbose_name='Создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 10, 36, 17, 189893, tzinfo=utc), verbose_name='Создан'),
            preserve_default=False,
        ),
    ]
