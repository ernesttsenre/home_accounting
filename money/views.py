from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from money.models import Operation, Account, Goal
from money.forms import OperationForm
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

    def form_valid(self, form):
        form.instance.account = self.account
        form.instance.user = self.user
        return super(OperationCreate, self).form_valid(form)
