# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0015_category_affected_limit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Основание', 'verbose_name_plural': 'Основания', 'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='account',
            name='credit_limit',
            field=models.DecimalField(max_digits=10, validators=[django.core.validators.MinValueValidator(1000, 'Если лимит есть, то он не может быть менее 1000')], null=True, verbose_name='Лимит пополнения', decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='credit_limit_period',
            field=models.CharField(verbose_name='Период для лимита пополнения', null=True, max_length=10, choices=[('month', 'Месяц'), ('week', 'Неделя'), ('day', 'День')], blank=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='created_at',
            field=models.DateTimeField(verbose_name='Создан'),
        ),
    ]
