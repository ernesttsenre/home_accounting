# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0020_auto_20150608_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='planitem',
            name='closed_at',
            field=models.DateTimeField(default='2015-01-01', verbose_name='Выполнена', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planitem',
            name='must_closed_at',
            field=models.DateTimeField(default='2015-01-01', verbose_name='Выполнить до', editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='planitem',
            name='period',
            field=models.CharField(choices=[('month', 'Каджый месяц'), ('week', 'Каждую неделю')], verbose_name='Повторять', max_length=10, default='month'),
        ),
        migrations.AlterField(
            model_name='planitem',
            name='state',
            field=models.CharField(choices=[('opened', 'Открыта'), ('closed', 'Выполнена')], verbose_name='Состояние', default='opened', max_length=10, editable=False),
        ),
    ]
