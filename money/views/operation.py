import json

from django.views.generic import MonthArchiveView, DetailView, CreateView
from django.shortcuts import get_object_or_404

from money.models import Operation, Account
from money.forms import OperationForm
from money.context_processors import global_vars


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


class OperationMonthArchiveView(MonthArchiveView):
    queryset = Operation.objects.credits()
    date_field = 'created_at'
    allow_future = True
    template_name = 'money/archive/operation_month.html'

    def get_context_data(self, **kwargs):
        context = super(OperationMonthArchiveView, self).get_context_data(**kwargs)

        # раздобудем данные для графика по тратам за неделю
        year = self.get_year()
        month = self.get_month()
        data = Operation.objects.get_credit_week_report(year, month)

        jsonData = {}
        jsonData['categories'] = json.dumps(data['categories'])
        jsonData['data'] = json.dumps(data['data'])

        # данные для графика трат по категориям
        pie = Operation.objects.get_credit_categories_month_report(year, month)
        jsonData['pie'] = json.dumps(pie['data'])

        # JSON для графиков
        context['graph'] = jsonData

        template_globals = global_vars(self.request)
        context['limit'] = template_globals['week_credit']['limit']
        context['amount'] = int(sum(data['data']))
        context['max'] = int(max(context['limit'], max(data['data'])))

        return context