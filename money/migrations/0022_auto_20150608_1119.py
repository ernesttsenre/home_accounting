# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0021_auto_20150608_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planitem',
            name='closed_at',
            field=models.DateTimeField(editable=False, verbose_name='Выполнена', null=True, blank=True),
        ),
    ]
