
from django.urls import path ,include
from .views import DepositMoneyView ,TransactionReportView

urlpatterns = [
     path('deposit/', DepositMoneyView.as_view(), name="deposit_money"),
     path('report/', TransactionReportView.as_view(), name="transaction_report"),
   
]