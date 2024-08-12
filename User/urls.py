
from django.urls import path 
from .views import UserRegistrationView ,UserLoginView , UserLogoutview ,UserLibraryAccountUpdateView,pass_change2
urlpatterns = [
    path('register/', UserRegistrationView.as_view() ,name='register'),
    path('login/',  UserLoginView.as_view(),name='login'),
    path('logout/', UserLogoutview.as_view() ,name='logout'),
    path('profile/', UserLibraryAccountUpdateView.as_view() ,name='profile'),
    path('pass_change2/',  pass_change2 ,name='passchange2'),  
   
]