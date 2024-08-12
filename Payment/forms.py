from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Transaction , UserLibraryAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount' , 'transaction_type']
    
    
    def __init__(self, *args , **kwargs):
        self.user_account = kwargs.pop('account') #account value k pop kore anlam
        super().__init__(*args , **kwargs)
        self.fields['transaction_type'].disabled = True #ai filed disabled thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe 



    def save(self, commit= True):
        self.instance.account = self.user_account
        self.instance.balance_after_transaction = self.instance.account.balance 
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self): #amount field k filter korlam
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') #User er fill up kora form theke amra amount field er value k neye aslam
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You need to deposit at least {min_deposit_amount} $')      
        return amount
    



