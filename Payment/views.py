from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import CreateView ,ListView
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from Payment.contants import DEPOSIT
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum
from datetime import datetime
from django.views import View
from django.shortcuts import get_object_or_404 , redirect
from django.urls import reverse_lazy
from django.core.mail import EmailMessage ,EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

  
def send_transaction_email(user ,amount ,subject ,template):
    message = render_to_string(template ,{'user':user,  'amount' : amount , })
    
    send_email = EmailMultiAlternatives( subject, '' , to=[user.email])
    send_email.attach_alternative(message ,'text/html')
    send_email.send()


class TransactionCreateMixin(CreateView ,LoginRequiredMixin):
    template_name = 'payment/transaction_form.html'
    model = Transaction
    title =''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs=  super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #template e context data pass kora
        context.update({
            'title' : self.title
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title ='Deposit'

    def get_initial(self):
        print('inside deposit')
        initial = {'transaction_type': DEPOSIT }  
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount # account balance = 500 , ami deposit korlam =1000, new balance holo = 1500
        account.save(
            update_fields = ['balance']
        )
        
        messages.success(self.request, f"${amount} was deposited to your account successfully")
        send_transaction_email( self.request.user ,amount ,'Deposite Message' ,'payment/deposite_email.html')
        return super().form_valid(form)


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'payment/transaction_report.html'
    model = Transaction
    balance = 0

    def get_queryset(self):
        queryset =  super().get_queryset().filter(
            account = self.request.user.account 
        )       

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(timestamp__date__gte = start_date ,timestamp__date__lte = end_date)
            
            self.balance = Transaction.objects.filter( timestamp__date__gte = start_date ,timestamp__date__lte = end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
        return queryset.distinct() #unique query set hote hobe
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #template e context data pass kora
        context.update({
            'account': self.request.user.account
        })
        return context

