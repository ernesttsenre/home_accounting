# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0006_auto_20150514_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.TextField(max_length=256, verbose_name='Название')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('created_at', models.DateTimeField(verbose_name='Создан', auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Цели',
                'verbose_name': 'Цель',
            },
        ),
        migrations.AlterField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(verbose_name='Создан', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(verbose_name='Создан', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='comment',
            field=models.TextField(null=True, verbose_name='Комментарий', blank=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='created_at',
            field=models.DateTimeField(verbose_name='Создан', auto_now_add=True),
        ),
        migrations.AddField(
            model_name='goal',
            name='account',
            field=models.ForeignKey(related_name='goals', on_delete='cascade', verbose_name='Счет', to='money.Account'),
        ),
    ]
