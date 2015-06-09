import easy

from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

from money.models import Account


class Transfer(models.Model):
    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    account_from = models.ForeignKey(
        Account,
        verbose_name='Счет кредитор',
        related_name='accounts_from',
        on_delete=models.CASCADE
    )

    account_to = models.ForeignKey(
        Account,
        verbose_name='Счет дебитор',
        related_name='accounts_to',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        validators=[
            validators.MinValueValidator(1, 'Сумма транзакции должна быть больше 0')
        ]
    )

    comment = models.TextField(
        verbose_name='Комментарий',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    @easy.short(desc='Название')
    def get_name(self):
        return "Перевод с счета: %s, на счет: %s" % (self.account_from.title, self.account_to.title)

    def clean(self):
        super(Transfer, self).clean()
        errors = {}

        if hasattr(self, 'account_from') and hasattr(self, 'account_to'):
            if self.account_from == self.account_to:
                errors['account_to'] = 'Перевод не выполнен - нельзя переводить деньги на тот же счет'

            amount = 0
            if self.amount:
                amount = self.amount

            account_from_balance = self.account_from.balance
            yet = account_from_balance - amount
            if yet < 0:
                errors['amount'] = 'Перевод не выполнен - недостаточно средств'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.get_name()
