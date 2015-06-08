# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0017_auto_20150605_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='credit_limit',
        ),
        migrations.RemoveField(
            model_name='account',
            name='credit_limit_period',
        ),
        migrations.RemoveField(
            model_name='account',
            name='debit_limit',
        ),
        migrations.RemoveField(
            model_name='account',
            name='debit_limit_period',
        ),
    ]
