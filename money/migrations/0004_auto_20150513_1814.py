# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_operation_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Счет', 'verbose_name_plural': 'Счета'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Основание', 'verbose_name_plural': 'Основания'},
        ),
        migrations.AlterModelOptions(
            name='operation',
            options={'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
        migrations.AddField(
            model_name='operation',
            name='comment',
            field=models.TextField(verbose_name='Комментарий', default=''),
        ),
        migrations.AlterField(
            model_name='operation',
            name='category',
            field=models.ForeignKey(verbose_name='Основание', to='money.Category'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='type',
            field=models.IntegerField(verbose_name='Тип операции', choices=[(1, 'Приход'), (-1, 'Расход')]),
        ),
    ]
