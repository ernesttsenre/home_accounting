from django import forms
from money.models import Operation


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
