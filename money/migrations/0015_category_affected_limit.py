# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0014_auto_20150601_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='affected_limit',
            field=models.BooleanField(default=True, verbose_name='Влияет на лимиты?'),
        ),
    ]
