import datetime

from django.db import models
from django.db.models import Count, Sum, F, FloatField
from django.db import connection
from django.core import validators
from django.contrib.humanize.templatetags.humanize import intcomma

from money.models import Param

class Account(models.Model):
    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'
        ordering = ['-balance']

    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Баланс',
        editable=False,
        default=0,
        validators=[
            validators.MinValueValidator(0, 'Недостаточно средств на счете')
        ]
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    def get_balance(self):
        aggregate = self.operations.all().aggregate(
            balance=Sum(F('amount') * F('type'), output_field=FloatField())
        )

        balance = 0
        if aggregate['balance']:
            balance = aggregate['balance']

        return balance

    def get_color(self):
        balance = self.balance

        if balance < 0:
            return 'danger'
        elif balance > 0:
            return 'primary'
        else:
            return 'default'

    def get_name(self):
        balance_string = intcomma(self.balance)
        return "%s (%s %s)" % (self.title, balance_string, 'руб.')

    def is_accumulation(self):
        accumulation_id = Param.get_param('accumulation_account')
        return self.id == int(accumulation_id)

    def get_available_credit_amount(self):
        if not self.credit_limit:
            return None

        cursor = connection.cursor()
        try:
            date = datetime.datetime.now()
            year = date.year

            condition = date.month
            if self.credit_limit_period == 'week':
                condition = date.isocalendar()[1]
            elif self.credit_limit_period == 'day':
                condition = date.today()

            cursor.execute('''
                SELECT
                  sum(money_operation.amount)
                FROM money_operation
                WHERE money_operation.type = -1 AND
                    extract(YEAR FROM money_operation.created_at) = %s AND
                    extract(%s FROM money_operation.created_at) = %s AND
                    money_operation.account_id = %s AND
                    money_operation.transfer_id IS NULL
            ''', [year, self.credit_limit_period, condition, self.id])

            rows = cursor.fetchone()

            credit_by_transaction = 0
            if len(rows) > 0 and rows[0]:
                credit_by_transaction = rows[0]

            transfer_amount = self.get_transfer_balance_by_period(self.credit_limit_period)
            if transfer_amount > 0 or not transfer_amount:
                transfer_amount = 0
            else:
                transfer_amount = abs(transfer_amount)

            credit_by_period = credit_by_transaction + transfer_amount

            # Текущий доступный лимит
            current_credit_limit = self.credit_limit - credit_by_period
            if current_credit_limit < 0:
                current_credit_limit = 0

            return current_credit_limit
        finally:
            cursor.close()

    @staticmethod
    def get_total_amount():
        total = 0
        accounts = Account.objects.all()
        for account in accounts:
            if not account.is_accumulation():
                total += account.balance
        return total

    def __str__(self):
        return self.get_name()