# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_auto_20150513_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='type',
            field=models.IntegerField(default=1, choices=[(1, 'debet'), (-1, 'credit')]),
            preserve_default=False,
        ),
    ]
