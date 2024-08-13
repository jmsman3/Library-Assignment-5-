from django.urls import path
from . import views

urlpatterns = [
     path('buy_book/<int:id>/', views.PurchaseBook_View.as_view(), name='buy_book'),
     path('return_book/<int:id>/', views.ReturnBook.as_view(), name='return_book'),
] 
