from django import forms
from django.forms.utils import ErrorList
from money.models import Operation, Transfer


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ('amount', 'type', 'category', 'comment', 'account', 'user')

        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма транзакции',
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
            }),

            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'user': forms.HiddenInput(),
            'account': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super(OperationForm, self).clean()
        amount = cleaned_data.get('amount')
        type = cleaned_data.get('type')
        account = cleaned_data.get('account')

        if type == Operation.CREDIT_OPERATION:
            account_balance = account.balance
            yet = account_balance - amount
            if yet < 0:
                self._errors['type'] = ErrorList()
                self._errors['type'].append('Операция не возможна - недостаточно средств')

        return cleaned_data



class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ('account_from', 'account_to', 'amount', 'comment')

        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма перевода',
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
            }),

            'account_from': forms.Select(attrs={'class': 'form-control'}),
            'account_to': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'user': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super(TransferForm, self).clean()
        account_from = cleaned_data.get('account_from')
        account_to = cleaned_data.get('account_to')
        amount = cleaned_data.get('amount')

        if account_from == account_to:
            self._errors['account_to'] = ErrorList()
            self._errors['account_to'].append('Перевод не выполнен - нельзя переводить деньги на тот же счет')
        else:
            account_from_balance = account_from.balance
            yet = account_from_balance - amount

            if yet < 0:
                self._errors['amount'] = ErrorList()
                self._errors['amount'].append('Перевод не выполнен - недостаточно средств')

        return cleaned_data
