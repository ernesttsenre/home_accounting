import datetime
import easy

from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

from money.models import Account, Transfer, Category, Goal
from money.managers import OperationManager


class Operation(models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    objects = OperationManager()

    CREDIT_OPERATION = -1
    DEBIT_OPERATION = 1
    OPERATION_TYPES = (
        (DEBIT_OPERATION, 'Приход'),
        (CREDIT_OPERATION, 'Расход'),
    )

    account = models.ForeignKey(
        Account,
        verbose_name='Счет',
        related_query_name='operations',
        related_name='operations',
        on_delete=models.CASCADE
    )

    transfer = models.ForeignKey(
        Transfer,
        verbose_name='Перевод',
        related_name='operations',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Основание',
        null=True,
        blank=True,
        related_name='operations'
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='operations',
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        validators=[
            validators.MinValueValidator(1, 'Сумма перевода должна быть больше 0'),
        ]
    )

    type = models.IntegerField(
        choices=OPERATION_TYPES,
        verbose_name='Тип операции'
    )

    comment = models.TextField(
        verbose_name='Комментарий',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.today()
        return super(Operation, self).save(*args, **kwargs)

    def get_amount(self):
        return str(self.amount * self.type)

    def get_color(self):
        if self.transfer:
            return 'info'

        if self.type < 0:
            return 'danger'
        return 'success'

    @easy.short(desc='Основание', order='category')
    def get_category_title(self):
        if self.category:
            title = self.category.title
        else:
            if self.transfer:
                if self.type == Operation.CREDIT_OPERATION:
                    title = "Перевод в %s" % self.transfer.account_to.title
                else:
                    title = "Перевод из %s" % self.transfer.account_from.title
            else:
                title = 'Неизвестно'

        return title

    @easy.short(desc='Сумма', order='amount')
    def get_name(self):
        return str(self.amount * self.type)

    @easy.short(desc='Перевод денег?', bool=True)
    def is_transfer(self):
        if self.transfer:
            return True
        return False

    def is_debit(self):
        return self.type == self.DEBIT_OPERATION

    def is_credit(self):
        return self.type == self.CREDIT_OPERATION

    def get_type_title(self):
        if self.type == self.CREDIT_OPERATION:
            return 'Расход'
        return 'Пополнение'

    def clean(self):
        super(Operation, self).clean()
        errors = {}

        if not self.id:
            if self.type == Operation.CREDIT_OPERATION:
                account_balance = self.account.balance
                yet = account_balance - self.amount
                if yet < 0:
                    errors['type'] = 'Операция не возможна - недостаточно средств'

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def get_credit_amount_by_this_week():
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        amount = 0
        items = Operation.objects.filter(
            created_at__range=[start_week, end_week],
            type=Operation.CREDIT_OPERATION,
            transfer_id__isnull=True,
            category__affected_limit=True
        )
        for item in items:
            amount += item.amount

        return amount

    def get_created_week(self):
        return self.created_at.isocalendar()[1]

    def __str__(self):
        return self.get_name()

