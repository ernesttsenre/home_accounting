# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0019_planitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planitem',
            name='period',
            field=models.CharField(null=True, verbose_name='Повторять', blank=True, max_length=10, choices=[('month', 'Каджый месяц'), ('week', 'Каждую неделю')]),
        ),
    ]
