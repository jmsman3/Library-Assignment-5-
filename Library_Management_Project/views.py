
from django.shortcuts import render , redirect
from Book.forms import BookForm ,BrandForm , CommentForm
from Book.models import BookModel , CategoryModel
from django.views.generic import DetailView 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
def home(request , category_slug = None):
    data = BookModel.objects.all()
    if category_slug is not None:
        category = CategoryModel.objects.get(slug = category_slug)
        data = BookModel.objects.filter( category_name = category )
    categories = CategoryModel.objects.all()
    print(data)
    return render(request , 'home.html', {'data' : data , 'category' : categories})