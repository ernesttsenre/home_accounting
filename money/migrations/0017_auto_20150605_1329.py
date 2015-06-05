# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0016_auto_20150605_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='debit_limit',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(1000, 'Если лимит есть, то он не может быть менее 1000')], decimal_places=2, verbose_name='Сумма', null=True, blank=True, max_digits=10),
        ),
        migrations.AddField(
            model_name='account',
            name='debit_limit_period',
            field=models.CharField(max_length=10, verbose_name='За какой период?', choices=[('month', 'Месяц'), ('week', 'Неделя'), ('day', 'День')], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='credit_limit',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(1000, 'Если лимит есть, то он не может быть менее 1000')], decimal_places=2, verbose_name='Сумма', null=True, blank=True, max_digits=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='credit_limit_period',
            field=models.CharField(max_length=10, verbose_name='За какой период?', choices=[('month', 'Месяц'), ('week', 'Неделя'), ('day', 'День')], blank=True, null=True),
        ),
    ]
