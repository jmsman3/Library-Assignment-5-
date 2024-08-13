
from django.db import models
from django.contrib.auth.models import User

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class BookModel(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    quantity = models.IntegerField(blank=True, null=True)
    category_name = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to='templates/media/uploads/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name}"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.buyer.username} of this Book - {self.book.title}"
        