import datetime
import easy

from django.db import models
from django.core import validators

from money.models import Account


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