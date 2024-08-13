from typing import Any
from django.shortcuts import render ,get_object_or_404
from Payment.models import Transaction
from Payment.forms import TransactionForm ,DepositForm
from Payment.views import TransactionCreateMixin
from  Borrowing.forms import PurchaseForm
from Payment.contants import PURCHASE ,RETURN
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Book.models import BookModel, Order
from Payment.models import Transaction
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from Payment.contants import PURCHASE 
from django.core.mail import EmailMessage ,EmailMultiAlternatives
from django.template.loader import render_to_string
from User.models import UserLibraryAccount
# from django.db import transaction as db_transaction  
from django.db import transaction as db_transaction  #

def send_transaction_email(user ,amount , book_title, subject ,template):
    message = render_to_string(template ,{'user':user,  'amount' : amount , 'book_title':book_title })
    
    send_email = EmailMultiAlternatives( subject, '' , to=[user.email])
    send_email.attach_alternative(message ,'text/html')
    send_email.send()


class PurchaseBook_View(View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(BookModel, id=book_id)
        user_account = request.user.account

        total_price = book.price
        book_title = book.title

        # Check user boi ta kinese and return kore nai
        existing_transaction = Transaction.objects.filter(
            book=book,
            account=user_account,
            transaction_type=PURCHASE,
            is_return=False
        ).exists()

        if existing_transaction:
            messages.error(request, f"You have already purchased this book: {book.title}. Check your Transaction Report for details.")
            return redirect('transaction_report')

        if user_account.balance < total_price:
            messages.error(request, "You don't have enough balance.")
            return redirect('purchase_failure')

        if book.quantity < 1:
            messages.error(request, "Book is out of stock.")
            return redirect('purchase_failure')

        with db_transaction.atomic():
            book.quantity -= 1
            book.save()

            user_account.balance -= total_price
            user_account.save()

            Transaction.objects.create(
                book=book,
                amount=total_price,
                account=user_account,
                balance_after_transaction=user_account.balance,
                transaction_type=PURCHASE
            )
            Order.objects.create(
                buyer = request.user,
                book  = book
            )
            messages.success(request, 'Congratulations, your purchase was successful!')

        send_transaction_email(request.user, total_price, book_title, 'Congratulations, Book Purchase Successful', 'borrowing/book_Purchase_email.html')
        return redirect('transaction_report')

class ReturnBook(View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(BookModel, id=book_id)
        user_account = request.user.account

        # check kori book already returne kina
        transaction = Transaction.objects.filter(book=book, account=user_account, transaction_type=PURCHASE, is_return=False).first()
        
        if not transaction:
            messages.error(request, "This book has already been returned.")
            return redirect('transaction_report')

        refund_amount = book.price
        book_title = book.title

        with db_transaction.atomic():  #
            # Update  quantity
            book.quantity += 1
            book.save()

            # Update account balance
            user_account.balance += refund_amount
            user_account.save()

           
            transaction.is_return = True
            transaction.save()
            Transaction.objects.create(
                book=book,
                amount=refund_amount,
                account=user_account,
                balance_after_transaction=user_account.balance,
                transaction_type=RETURN,
            )

        messages.success(request, 'The book has been returned and the amount has been added to your balance.')
        send_transaction_email(self.request.user, refund_amount, book_title, 'Book Return Successful', 'borrowing/book_Return_email.html')
        return redirect('transaction_report')




# class ReturnBook(View):
#     def post(self , request, *args , **kwargs):
#         book_id = kwargs.get('id')
#         book = get_object_or_404(BookModel, id=book_id)
#         user_account = request.user.account
#         total_price = book.price

#         user_account.balance += total_price
#         user_account.save()
#         return redirect('transaction_report')
    
  
