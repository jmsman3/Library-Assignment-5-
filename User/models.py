from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from .constant import GENDER_TYPE
# Create your models here.


class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User , related_name='account', on_delete=models.CASCADE)
    account_no = models.CharField(unique=True , max_length=10) #account name duijon user er same hobe na
    reference_code = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True) #ke o faka rakhle o somossa nai
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2 ) # ekjon user 12 digit obdi taka rakhte parbe and dui dosomik porjonto taka rakhte parbe jemon 1000.50

    def __str__(self):
        return str(self.account_no)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User , related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code =models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.email)
        