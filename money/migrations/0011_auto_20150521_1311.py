# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0010_auto_20150521_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.DecimalField(verbose_name='Баланс', default=0, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goal',
            name='account',
            field=models.ForeignKey(related_name='goals', to='money.Account', verbose_name='Счет'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='account',
            field=models.ForeignKey(related_name='operations', to='money.Account', verbose_name='Счет'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='transfer',
            field=models.ForeignKey(related_name='transfers', editable=False, to='money.Transfer', blank=True, verbose_name='Перевод', null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='account_from',
            field=models.ForeignKey(related_name='accounts_from', to='money.Account', verbose_name='Счет кредитор'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='account_to',
            field=models.ForeignKey(related_name='accounts_to', to='money.Account', verbose_name='Счет дебитор'),
        ),
    ]
