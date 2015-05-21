from django import forms
from money.models import Operation, Transfer


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ('amount', 'type', 'category', 'comment')

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
