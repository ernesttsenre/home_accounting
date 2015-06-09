import easy

from django.db import models
from django.core import validators

from money.models import Account


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['amount']

    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        validators=[
            validators.MinValueValidator(1, 'Сумма цели должна быть больше 0')
        ]
    )

    percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Достижение',
        editable=False,
        default=0
    )

    account = models.ForeignKey(
        Account,
        verbose_name='Счет',
        related_name='goals',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    @easy.short(desc='Достижение')
    def get_percent(self):
        account_balance = self.account.get_balance()
        percent = float(account_balance * 100) / float(self.amount)
        return int(percent)

    def get_color(self):
        percent = self.get_percent()
        if percent > 90:
            return 'danger'
        elif percent > 50:
            return 'warning'
        else:
            return 'success'