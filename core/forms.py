from django import forms
from models import Expense, Item

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description']