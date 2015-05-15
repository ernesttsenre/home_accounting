# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0007_auto_20150515_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Название'),
        ),
    ]
