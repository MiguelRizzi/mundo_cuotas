from django.contrib import admin
from .models import Product, File, Category
# Register your models here.

admin.site.register(Product)
admin.site.register(File)
admin.site.register(Category)