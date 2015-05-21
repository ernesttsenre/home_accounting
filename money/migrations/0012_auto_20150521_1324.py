# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0011_auto_20150521_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='percent',
            field=models.DecimalField(verbose_name='Сумма', editable=False, max_digits=10, default=0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(verbose_name='Баланс', editable=False, max_digits=10, default=0, decimal_places=2),
        ),
    ]
