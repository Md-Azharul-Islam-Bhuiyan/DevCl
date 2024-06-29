from django.contrib import admin
from apps.product.models import Category, SubCategory, Brand, Product
# Register your models here.


admin.site.register(Category),
admin.site.register(SubCategory),
admin.site.register(Brand),
admin.site.register(Product)