from django.shortcuts import render
from Payment.models import Transaction
from Payment.forms import TransactionForm ,DepositForm 
from django.core.exceptions import ValidationError
from django import forms
class PurchaseForm(TransactionForm):
    class Meta:
        model = Transaction
        fields = ['amount' , 'transaction_type']
    
    def clean_amount(self):
        account_balance = self.user_account.balance
        amount = self.cleaned_data.get('amount')

        if amount > account_balance:
            raise forms.ValidationError('Sorry ,You do not have sufficient balance to buy the book')
        return amount 