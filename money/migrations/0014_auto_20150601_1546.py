# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0013_auto_20150601_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='param',
            name='title',
            field=models.CharField(verbose_name='Название', default='title', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='param',
            name='key',
            field=models.CharField(verbose_name='Ключ', max_length=256),
        ),
    ]
