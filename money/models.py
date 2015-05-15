from django.db import models
from django.db.models import Sum, F, FloatField
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma

class Account(models.Model):
    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    title = models.CharField(max_length=256, verbose_name='Название')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    def get_balance(self):
        aggregate = self.operations.all().aggregate(
            balance=Sum(F('amount') * F('type'), output_field=FloatField())
        )

        balance = 0
        if aggregate['balance']:
            balance = aggregate['balance']

        return balance

    def get_color(self):
        balance = self.get_balance()

        if balance < 0:
            return 'danger'
        elif balance > 0:
            return 'success'
        else:
            return 'default'

    def __str__(self):
        balance_string = intcomma(self.get_balance())
        return "%s (%s %s)" % (self.title, balance_string, 'руб.')


class Category(models.Model):
    class Meta:
        verbose_name = 'Основание'
        verbose_name_plural = 'Основания'

    title = models.CharField(max_length=256, verbose_name='Название')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    def __str__(self):
        return self.title


class Operation(models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    OPERATION_TYPES = (
        (1, 'Приход'),
        (-1, 'Расход'),
    )

    account = models.ForeignKey(Account, verbose_name='Счет', related_name='operations', on_delete='cascade')
    category = models.ForeignKey(Category, verbose_name='Основание')
    user = models.ForeignKey(User, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    type = models.IntegerField(choices=OPERATION_TYPES, verbose_name='Тип операции')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    def get_amount(self):
        return self.amount * self.type

    def get_color(self):
        if self.type < 0:
            return 'danger'
        return 'success'

    def description(self):
        return self

    def __str__(self):
        return str(self.amount * self.type)

class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(max_length=256, verbose_name='Название')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    account = models.ForeignKey(Account, verbose_name='Счет', related_name='goals', on_delete='cascade')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    def get_percent(self):
        account_balance = self.account.get_balance()
        percent = float(account_balance * 100) / float(self.amount)
        return int(percent)

    def get_color(self):
        percent = self.get_percent()
        if percent > 80:
            return 'danger'
        elif percent > 50:
            return 'warning'
        elif percent > 25:
            return 'success'
        else:
            return 'info'

