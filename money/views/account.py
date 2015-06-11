from django.views.generic import ListView, DetailView
from datetime import datetime, timedelta

from money.models import Account, Goal


class AccountList(ListView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)

        goals = Goal.objects.all()
        context['goals'] = goals
        context['goals_total'] = Goal.get_total_amount()

        total_balance = Account.get_total_amount()
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