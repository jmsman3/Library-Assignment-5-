from django.contrib import admin
from Book.models import BookModel ,CategoryModel ,Comment ,Order
# Register your models here.
admin.site.register(BookModel)
# admin.site.register(CategoryModel )

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name' ,)}
    list_display = ['name' , 'slug']

admin.site.register( CategoryModel , CategoryAdmin)
admin.site.register( Comment)
admin.site.register( Order)