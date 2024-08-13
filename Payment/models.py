from django.db import models
from User.models import UserLibraryAccount
from Payment.contants import TRANSACTIONS_TYPE
from Book.models import BookModel
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserLibraryAccount,on_delete=models.CASCADE,related_name='transactions') #ekjon user er multiple transactions hote pare 
    amount = models.DecimalField(decimal_places=2, max_digits=12)  
    balance_after_transaction= models.DecimalField(decimal_places=2,max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTIONS_TYPE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE , null=True , blank=True )
    is_return = models.BooleanField(default=False)
    
 
   
    
    class Meta:
        ordering = ['timestamp']
        