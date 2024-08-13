

from django.shortcuts import render, redirect, get_object_or_404
from Book.forms import BookForm, BrandForm, CommentForm
from Book.models import BookModel, Order, CategoryModel
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
    return render(request , 'home.html', {'data' : data , 'category' : categories})


@login_required
def book_post(request):
    if request.method == 'POST': 
        post_form = BookForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('home')
    else:
        post_form = BookForm()
    return render(request, 'book_plate/post.html', {'form': post_form})

@login_required
def brand_post(request):
    if request.method == 'POST': 
        post_form = BrandForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('Bookpost')
    else:
        post_form = BrandForm()
    return render(request, 'book_plate/add_brand.html', {'form': post_form})

@method_decorator(login_required, name='dispatch')
class DetailPostView(DetailView):
    model = BookModel
    pk_url_kwarg = 'id'
    template_name ='book_plate/detail_post.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = CommentForm()
        
        purchase_person=Order.objects.filter( buyer=self.request.user , book=post ).exists()

        context['comments'] = comments
        context['comment_form'] = comment_form
        context['purchase_person'] = purchase_person    

        return context
    


@login_required
def buy_book(request, id):
    book = get_object_or_404(BookModel, pk=id)
    if book.quantity is not None and book.quantity > 0:
        book.quantity -= 1
        book.save()
        Order.objects.create(buyer=request.user, book=book)
        messages.success(request, 'You have successfully bought the book')
    else:
        messages.warning(request, 'Sorry, the book is out of stock')
    return redirect('home')

@login_required
def profile(request):
    orders = Order.objects.filter(buyer=request.user)
    return render(request, 'book_plate/book_profile.html', {'purchases': orders})
