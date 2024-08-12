from django.urls import path
from . import views

urlpatterns = [
     path('buy_book/<int:id>/', views.PurchaseBook_View.as_view(), name='buy_book'),
] 
