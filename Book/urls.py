
from django.urls import path ,include
from .import views


urlpatterns = [

    path('profile/', views.profile ,name='profile'), 

    path('category/<slug:category_slug>/',views.home  , name='category_wise_post'),
    path('Bookpost/', views.book_post ,name='Bookpost'),
    path('brandpost/', views.brand_post ,name='brandpost'),
    path('detail/<int:id>/', views.DetailPostView.as_view(),name='detail'),
    
    path('buy_Book_quantity/<int:id>/', views.buy_book,name='buy_Book_quantity'),
]