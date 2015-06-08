import json
import datetime
import easy

from money.managers import OperationManager

from django.db import models
from django.db import connection
from django.db.models import Count, Sum, F, FloatField
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models.signals import post_save, post_delete
from django.core import validators
from django.core.exceptions import ValidationError


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


class Category(models.Model):
    class Meta:
        verbose_name = 'Основание'
        verbose_name_plural = 'Основания'
        ordering = ['title']

    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )

    affected_limit = models.BooleanField(
        verbose_name='Влияет на лимиты?',
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    def __str__(self):
        return self.title


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
        related_name='operations',
        on_delete=models.CASCADE
    )

    transfer = models.ForeignKey(
        Transfer,
        verbose_name='Перевод',
        related_name='transfers',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Основание',
        null=True,
        blank=True
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
            if self.type == Operation.CREDIT_OPERATION:
                title = "Перевод в %s" % self.transfer.account_to.title
            else:
                title = "Перевод из %s" % self.transfer.account_from.title

        return title

    @easy.short(desc='Сумма', order='amount')
    def get_name(self):
        return str(self.amount * self.type)

    @easy.short(desc='Перевод денег?', bool=True)
    def is_transfer(self):
        if self.transfer:
            return True
        return False

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


class Param(models.Model):
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    title = models.CharField(max_length=256, verbose_name='Название')
    key = models.CharField(max_length=256, verbose_name='Ключ')
    value = models.CharField(max_length=512, verbose_name='Значение')

    @staticmethod
    def get_params():
        params = {}
        items = Param.objects.all()

        for item in items:
            params[item.key] = item.value

        return params

    @staticmethod
    def get_param(key):
        params = Param.get_params()
        if params[key]:
            return params[key]

        return None


class PlanItem(models.Model):
    class Meta:
        verbose_name = 'Плановые траты'
        verbose_name_plural = 'Плановые траты'
        ordering = ['created_at', 'state']

    PERIOD_MONTH = 'month'
    PERIOD_WEEK = 'week'
    PERIOD_OPTIONS = (
        (PERIOD_MONTH, 'Каджый месяц'),
        (PERIOD_WEEK, 'Каждую неделю'),
    )

    STATE_OPENED = 'opened'
    STATE_CLOSED = 'closed'
    STATE_OPTIONS = (
        (STATE_OPENED, 'Открыта'),
        (STATE_CLOSED, 'Выполнена'),
    )

    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    account = models.ForeignKey(
        Account,
        verbose_name='Счет'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма',
        validators=[
            validators.MinValueValidator(1, 'Сумма цели должна быть больше 0')
        ]
    )
    period = models.CharField(
        max_length=10,
        choices=PERIOD_OPTIONS,
        verbose_name='Повторять',
        default=PERIOD_MONTH
    )
    state = models.CharField(
        max_length=10,
        choices=STATE_OPTIONS,
        verbose_name='Состояние',
        default=STATE_OPENED,
        editable=False
    )
    alert_on_main = models.BooleanField(
        verbose_name='Показывать напоминание на главном экране',
        default=True
    )
    must_closed_at = models.DateTimeField(
        verbose_name='Выполнить до',
        editable=False
    )
    closed_at = models.DateTimeField(
        verbose_name='Выполнена',
        editable=False,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )

    def mark_closed(self):
        self.state = self.STATE_CLOSED
        self.closed_at = datetime.datetime.now()

    @easy.short(desc='Выполнено?', bool=True)
    def is_closed(self):
        return self.state == self.STATE_CLOSED

    def calc_must_closed(self, from_closed=False):
        if not from_closed:
            date = datetime.datetime.now()
        else:
            date = self.must_closed_at

        period = self.period
        if period == self.PERIOD_MONTH:
            month = date.month + 1
            self.must_closed_at = datetime.date(date.year, month, 1)
        elif period == self.PERIOD_WEEK:
            self.must_closed_at = date + datetime.timedelta(week=1)

    @staticmethod
    def get_overdue():
        return PlanItem.objects.filter(
            closed_at__isnull=True,
            must_closed_at__lt=datetime.datetime.now()
        )

    def save(self, *args, **kwargs):
        if self.must_closed_at is None:
            self.calc_must_closed()
        return super(PlanItem, self).save(*args, **kwargs)



def create_transfer_operations(sender, instance, **kwargs):
    Operation.objects.filter(transfer_id=instance.id).delete()

    credit_operation = Operation()
    credit_operation.account = instance.account_from
    credit_operation.transfer = instance
    credit_operation.user = instance.user
    credit_operation.amount = instance.amount
    credit_operation.type = Operation.CREDIT_OPERATION
    credit_operation.save()

    debit_operation = Operation()
    debit_operation.account = instance.account_to
    debit_operation.transfer = instance
    debit_operation.user = instance.user
    debit_operation.amount = instance.amount
    debit_operation.type = Operation.DEBIT_OPERATION
    debit_operation.save()


def create_operation(sender, instance, **kwargs):
    instance.account.balance = instance.account.get_balance()
    instance.account.save()

    goals = Goal.objects.filter(account_id=instance.account.id)
    for goal in goals:
        goal.percent = goal.get_percent()
        goal.save()


def delete_operation(sender, instance, **kwargs):
    instance.account.balance = instance.account.get_balance()
    instance.account.save()

    goals = Goal.objects.filter(account_id=instance.account.id)
    for goal in goals:
        goal.percent = goal.get_percent()
        goal.save()


post_save.connect(create_transfer_operations, sender=Transfer)
post_save.connect(create_operation, sender=Operation)
post_delete.connect(create_operation, sender=Operation)
