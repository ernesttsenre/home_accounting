# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0012_auto_20150521_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('key', models.CharField(verbose_name='Параметр', max_length=256)),
                ('value', models.CharField(verbose_name='Значение', max_length=512)),
            ],
            options={
                'verbose_name': 'Параметр',
                'verbose_name_plural': 'Параметры',
            },
        ),
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Счет', 'ordering': ['-balance'], 'verbose_name_plural': 'Счета'},
        ),
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Цель', 'ordering': ['amount'], 'verbose_name_plural': 'Цели'},
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(0, 'Недостаточно средств на счете')], max_digits=10, default=0, verbose_name='Баланс', decimal_places=2, editable=False),
        ),
        migrations.AlterField(
            model_name='goal',
            name='amount',
            field=models.DecimalField(decimal_places=2, verbose_name='Сумма', validators=[django.core.validators.MinValueValidator(1, 'Сумма цели должна быть больше 0')], max_digits=10),
        ),
        migrations.AlterField(
            model_name='goal',
            name='percent',
            field=models.DecimalField(decimal_places=2, verbose_name='Достижение', editable=False, max_digits=10, default=0),
        ),
        migrations.AlterField(
            model_name='operation',
            name='amount',
            field=models.DecimalField(decimal_places=2, verbose_name='Сумма', validators=[django.core.validators.MinValueValidator(1, 'Сумма перевода должна быть больше 0')], max_digits=10),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='amount',
            field=models.DecimalField(decimal_places=2, verbose_name='Сумма', validators=[django.core.validators.MinValueValidator(1, 'Сумма транзакции должна быть больше 0')], max_digits=10),
        ),
    ]
