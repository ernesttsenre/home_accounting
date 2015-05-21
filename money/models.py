from django.db import models
from django.db.models import Sum, F, FloatField
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models.signals import post_save
import easy


class Account(models.Model):
    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    title = models.CharField(max_length=256, verbose_name='Название')
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Баланс', editable=False, default=0)
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

    def get_name(self):
        balance_string = intcomma(self.get_balance())
        return "%s (%s %s)" % (self.title, balance_string, 'руб.')

    def __str__(self):
        return self.get_name()


class Category(models.Model):
    class Meta:
        verbose_name = 'Основание'
        verbose_name_plural = 'Основания'

    title = models.CharField(max_length=256, verbose_name='Название')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    def __str__(self):
        return self.title


class Transfer(models.Model):
    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    account_from = models.ForeignKey(Account, verbose_name='Счет кредитор', related_name='accounts_from',
                                     on_delete=models.CASCADE)
    account_to = models.ForeignKey(Account, verbose_name='Счет дебитор', related_name='accounts_to',
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    @easy.short(desc='Название')
    def get_name(self):
        return "Перевод с счета: %s, на счет: %s" % (self.account_from.title, self.account_to.title)

    def __str__(self):
        return self.get_name()


class Operation(models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    CREDIT_OPERATION = -1
    DEBIT_OPERATION = 1
    OPERATION_TYPES = (
        (DEBIT_OPERATION, 'Приход'),
        (CREDIT_OPERATION, 'Расход'),
    )

    account = models.ForeignKey(Account, verbose_name='Счет', related_name='operations', on_delete=models.CASCADE)
    transfer = models.ForeignKey(Transfer, verbose_name='Перевод', related_name='transfers', on_delete=models.CASCADE,
                                 null=True, blank=True, editable=False)
    category = models.ForeignKey(Category, verbose_name='Основание', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    type = models.IntegerField(choices=OPERATION_TYPES, verbose_name='Тип операции')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

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
        title = 'Перевод'
        if self.category:
            title = self.category.title
        return title

    @easy.short(desc='Сумма', order='amount')
    def get_name(self):
        return str(self.amount * self.type)

    @easy.short(desc='Перевод денег?', bool=True)
    def is_transfer(self):
        if self.transfer:
            return True
        return False

    def __str__(self):
        return self.get_name()


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    title = models.CharField(max_length=256, verbose_name='Название')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    percent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Достижение', editable=False, default=0)
    account = models.ForeignKey(Account, verbose_name='Счет', related_name='goals', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    @easy.short(desc='Достижение')
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


post_save.connect(create_transfer_operations, sender=Transfer)
post_save.connect(create_operation, sender=Operation)
