# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0018_auto_20150608_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Название', max_length=256)),
                ('amount', models.DecimalField(max_digits=10, verbose_name='Сумма', decimal_places=2, validators=[django.core.validators.MinValueValidator(1, 'Сумма цели должна быть больше 0')])),
                ('period', models.CharField(verbose_name='Повторять', default='month', max_length=10, choices=[('month', 'Каджый месяц'), ('week', 'Каждую неделю')])),
                ('state', models.CharField(verbose_name='Состояние', default='opened', max_length=10, choices=[('opened', 'Открыта'), ('closed', 'Выполнена')])),
                ('alert_on_main', models.BooleanField(default=True, verbose_name='Показывать напоминание на главном экране')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('account', models.ForeignKey(to='money.Account', verbose_name='Счет')),
            ],
            options={
                'verbose_name': 'Плановые траты',
                'verbose_name_plural': 'Плановые траты',
                'ordering': ['created_at', 'state'],
            },
        ),
    ]
