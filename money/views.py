import json
from money.context_processors import global_vars

from django.views.generic import MonthArchiveView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from money.models import Operation, Account, Goal, Transfer
from money.forms import OperationForm, TransferForm
from datetime import datetime, timedelta


class AccountList(ListView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)

        goals = Goal.objects.all()
        context['goals'] = goals

        total_balance = 0
        accounts = self.model.objects.all()
        for account in accounts:
            total_balance += account.get_balance()

        context['total'] = total_balance
        return context


class AccountDetail(DetailView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super(AccountDetail, self).get_context_data(**kwargs)

        last_month = datetime.today() - timedelta(days=30)
        operations = self.object.operations.filter(created_at__gte=last_month).order_by('-created_at')

        context['operations'] = operations
        return context


class OperationDetail(DetailView):
    model = Operation


class OperationCreate(CreateView):
    form_class = OperationForm
    template_name = 'money/operation_create.html'
    account = None
    user = None

    def get_initial(self):
        self.account = get_object_or_404(Account, pk=self.kwargs.get('account_id'))
        self.user = self.request.user
        self.success_url = "/account/%s" % self.account.id
        return {
            'account': self.account,
            'user': self.user
        }

    def get_context_data(self, **kwargs):
        context = super(OperationCreate, self).get_context_data(**kwargs)
        context['account'] = self.account
        return context


class TransferCreate(CreateView):
    form_class = TransferForm
    template_name = 'money/transfer_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransferCreate, self).form_valid(form)


class OperationMonthArchiveView(MonthArchiveView):
    queryset = Operation.objects.credits()
    date_field = 'created_at'
    allow_future = True
    template_name = 'money/archive/operation_month.html'

    def get_context_data(self, **kwargs):
        context = super(OperationMonthArchiveView, self).get_context_data(**kwargs)

        # раздобудем данные для графика
        year = self.get_year()
        month = self.get_month()
        data = Operation.objects.get_credit_week_report(year, month)

        data['categories'] = json.dumps(data['categories'])
        data['data'] = json.dumps(data['data'])
        context['graph'] = data

        template_globals = global_vars(self.request)
        context['limit'] = template_globals['week_credit']['limit']
        context['amount'] = template_globals['week_credit']['amount']

        max = context['limit']
        if context['amount'] >= context['limit']:
            max = context['amount'] + 500
        context['max'] = max

        return context
