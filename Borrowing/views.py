from typing import Any
from django.shortcuts import render ,get_object_or_404
from Payment.models import Transaction
from Payment.forms import TransactionForm ,DepositForm
from Payment.views import TransactionCreateMixin
from  Borrowing.forms import PurchaseForm
from Payment.contants import PURCHASE
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Book.models import BookModel, Order
from Payment.models import Transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View



class PurchaseBook_View(View):
    title = 'Purchase Book'
    def get_form_kwargs(self):
        kwargs=  super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['transaction_type'] = PURCHASE
        return initial
    
    def form_valid(self, form):
        book_id = self.kwargs.get('id')
        
        book_id = get_object_or_404(BookModel, pk=id)
        if book_id.quantity is not None and book_id.quantity > 0:
            book_id.quantity -= 1
            book_id.save()
            Order.objects.create(buyer=self.request.user, book=book_id)
            messages.success(self.request, 'You have successfully bought the book')

        amount = form.cleaned_data['amount']
        account = self.request.user.account

        account.balance -= amount
        account.save(update_fields=['balance'])
        messages.success(self.request , f"Purchase successful..! Now ,${amount}deducted from your account.")
        
        return super().form_valid(form)
    
    
    
# from django.shortcuts import get_object_or_404, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

# class PurchaseBook_View(TransactionCreateMixin):
#     form_class = PurchaseForm
#     title = 'Purchase Book'
    
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get_initial(self):
#         initial = super().get_initial()
#         initial['transaction_type'] = PURCHASE
#         return initial
    
#     def form_valid(self, form):
#         amount = form.cleaned_data['amount']
#         account = self.request.user.account
        
#         # Deduct the amount from the user's balance
#         if account.balance >= amount:
#             account.balance -= amount
#             account.save(update_fields=['balance'])
#             messages.success(self.request, f"Purchase successful! Now, ${amount} has been deducted from your account.")
            
#             # Handle book purchase logic
#             book_id = self.kwargs.get('id')
#             book = get_object_or_404(BookModel, pk=book_id)
#             if book.quantity is not None and book.quantity > 0:
#                 book.quantity -= 1
#                 book.save()
#                 Order.objects.create(buyer=self.request.user, book=book)
#                 messages.success(self.request, 'You have successfully bought the book')
#             else:
#                 messages.warning(self.request, 'Sorry, the book is out of stock')
#                 return redirect('home')

#         else:
#             messages.warning(self.request, 'Insufficient balance to complete the purchase.')
#             return redirect('home')
        
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return redirect('home')  # Or any other URL you want to redirect to after a successful purchase


# @login_required
# class BuyBookView(TransactionCreateMixin):
#     def post(self, request, id):
#         book = get_object_or_404(BookModel, pk=id)
#         account = request.user.account 

#         if book.quantity is None or book.quantity <= 0:
#             messages.warning(request, 'Sorry, the book is out of stock.')
#             return redirect('home')

#         if account.balance < int(book.price):          
#             messages.warning(request, 'Insufficient Balance. Please deposit more money into your account.')
#             return redirect('home')

#         book.quantity -= 1
#         book.save()

#         account.balance -= int(book.price)
#         account.save(update_fields=['balance'])
        
#         Order.objects.create(buyer=request.user, book=book)   
#         Transaction.objects.create(user=request.user, amount=book.price, transaction_type=PURCHASE)

#         messages.success(request, 'You have successfully bought the book and the amount has been deducted from your account.')        
#         return redirect('home')

