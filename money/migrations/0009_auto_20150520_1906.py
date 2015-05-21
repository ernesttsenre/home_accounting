# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0008_auto_20150515_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('amount', models.DecimalField(verbose_name='Сумма', decimal_places=2, max_digits=10)),
                ('comment', models.TextField(verbose_name='Комментарий', blank=True, null=True)),
                ('created_at', models.DateTimeField(verbose_name='Создан', auto_now_add=True)),
                ('account_from', models.ForeignKey(on_delete='cascade', verbose_name='Счет кредитор', related_name='accounts_from', to='money.Account')),
                ('account_to', models.ForeignKey(on_delete='cascade', verbose_name='Счет дебитор', related_name='accounts_to', to='money.Account')),
            ],
            options={
                'verbose_name': 'Перевод',
                'verbose_name_plural': 'Переводы',
            },
        ),
        migrations.AddField(
            model_name='operation',
            name='transfer',
            field=models.ForeignKey(to='money.Transfer', on_delete='cascade', verbose_name='Перевод', related_name='transfers', null=True, blank=True),
        ),
    ]
