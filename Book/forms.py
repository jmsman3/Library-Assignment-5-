from Book.models import BookModel , CategoryModel ,Comment
from django import forms
class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'
        # exclude = ['author']

class BrandForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        # fields = '__all__'
        exclude = ['slug']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name' , 'email' , 'body']
        
