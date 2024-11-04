from django.contrib import admin
from .models import category,SubCategory,product
# Register your models here.
admin.site.register(category)
admin.site.register(SubCategory)
admin.site.register(product)