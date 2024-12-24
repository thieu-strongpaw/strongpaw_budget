from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_date', 'amount', 'account', 'category', 'notes']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'account': forms.Select(),
            'category': forms.Select(),
            'notes': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
